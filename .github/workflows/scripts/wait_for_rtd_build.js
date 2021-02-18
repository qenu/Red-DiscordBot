module.exports = (async function ({github, context}) {
    const rtd_api_token = process.env.RTD_API_TOKEN;
    const commit = context.sha;
    const poll_rate = 10 * 1000; // 10 seconds
    const timeout = 15 * 60 * 1000; // 15 minutes
    const deadline = new Date().getTime() + timeout;

    while (new Date().getTime() <= deadline) {
        // sleeping at the beginning to ensure RTD gets the memo about the new tag
        await new Promise(r => setTimeout(r, sleep_time));

        console.log(`Retrieving pending RTD builds for commit ${commit}...`);
        // make request here
        try {
            data = await new Promise(function (resolve, reject) {
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function() {
                    if (xhr.readyState == 4) {
                        if (status == 200)
                            resolve(JSON.parse(xhr.responseText));
                        else
                            reject({status: status, text: xhr.responseText});
                    }
                }
                xhr.open(
                    'GET',
                    `https://readthedocs.org/api/v3/projects/red-discordbot/builds/?running=true&commit=${commit}`,
                    false,
                );
                xhr.setRequestHeader('Authorization', `Token ${rtd_api_token}`);
                xhr.send(null);
            });
        } catch ({status, text}) {
            core.setFailed(
                `API request to RTD API failed with status code ${status} and response:\n${text}`
            );
            return;
        }

        if (!data["results"]) {
            console.log(`All RTD builds for commit ${commit} have finished.`);
            return;
        }

        console.log(`Pending RTD builds for commit ${commit}, waiting for 10 seconds...`);
    }

    core.setFailed('Waiting for RTD build to finish timed out.');
})
