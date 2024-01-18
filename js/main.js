function openWebApp() {
    document.getElementById("app-intro").style.display = "none";
    document.getElementById("sketch").style.display = "block";

    const scriptTag = document.createElement("script");
    scriptTag.type = "py";
    scriptTag.src = "viz.pyscript";
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


function main() {
    const tabs = new Tabby("[data-tabs]");

    document.getElementById("open-web-app-button").addEventListener("click", openWebApp);
}


main();