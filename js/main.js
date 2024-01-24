/**
 * Logic for running the overarching web application in which the visualization application sits.
 * 
 * @license BSD
 */

/**
 * Start the web application.
 */
function openWebApp() {
    document.getElementById("app-intro").style.display = "none";
    document.getElementById("sketch").style.display = "block";

    const scriptTag = document.createElement("script");
    scriptTag.type = "py";
    scriptTag.src = "viz.pyscript?v=0.1.2";
    document.getElementById("sketch").appendChild(scriptTag);

    document.getElementById("app").classList.add("center");

    let progress = 0;
    const progressBar = document.getElementById("sketch-load-progress");
    progressBar.value = 0;
    const incrementBar = () => {
        progressBar.value += 1;

        if (progressBar.value < 19) {
            setTimeout(incrementBar, 500);
        }
    };
    incrementBar();
}


/**
 * Driver entrypoint.
 */
function main() {
    const tabs = new Tabby("[data-tabs]");

    document.getElementById("open-web-app-button").addEventListener("click", openWebApp);
    document.addEventListener('tabby', (event) => {
        const tab = event.target;
        window.location.hash = new URL(tab.href).hash;
    }, false);
    window.addEventListener("hashchange", (event) => {
        const targetUrl = new URL(window.location.href).hash;
        tabs.toggle(targetUrl);
        event.preventDefault();
    });
}


main();