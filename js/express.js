const EXPORT_URL = "https://6saet4fqci.execute-api.us-east-2.amazonaws.com/default/gafj-topic-explorer-export";
const STATS_URL = "https://g69mcjf2re.execute-api.us-east-2.amazonaws.com/default/gafj-topic-explorer-stat";


function isAll(target) {
    return target === "all" || target === "All" || target === "";
}


function getQueryParam(elementId) {
    const name = elementId.split("-")[0];
    const value = document.getElementById(elementId).value;
    return {"name": name, "value": value};
}


function getQueryParamsStr() {
    const elements = [
        getQueryParam("country-select"),
        getQueryParam("category-select"),
        getQueryParam("tag-select"),
        getQueryParam("keyword-input"),
        getQueryParam("dimension-select")
    ];

    const validElements = elements.filter((x) => !isAll(x["value"]));
    const elementStrs = validElements.map((x) => x["name"] + "=" + encodeURIComponent(x["value"]));
    return elementStrs.join("&");
}


function executeExport() {
    const targetUrl = EXPORT_URL + "?" + getQueryParamsStr();
    window.open(targetUrl, '_blank');
}


function updateReport(rows) {
    rows.sort((a, b) => b["percent"] - a["percent"]);

    const reportSelection = d3.select("#express-report");
    reportSelection.html("");

    const table = reportSelection.append("table").classed("express-results", true);
    const tableHead = table.append("thead");
    const tableHeadRow = tableHead.append("tr");
    tableHeadRow.append("th").html("Name");
    tableHeadRow.append("th").html("Percent");

    const tableBody = table.append("tbody");
    const tableRows = tableBody.selectAll("tr").data(rows).enter().append("tr");
    tableRows.append("td").text((x) => x["name"]);
    
    const dataCells = tableRows.append("td");
    dataCells.append("div").classed("data-label", true).html((x) => Math.round(x["percent"]) + "%");
    dataCells.append("div").classed("data-bar", true).style("width", (x) => {
        const numPixels = x["percent"] / 100 * 300;
        return numPixels + "px";
    });

    document.getElementById("express-status").innerHTML = "Loaded.";
    document.getElementById("execute-express-button").style.display = "inline-block";
    document.getElementById("express-loading").style.display = "none";
}


function convertRow(rawRow) {
    return {
        "name": rawRow["name"],
        "percent": parseFloat(rawRow["percent"]) * 100
    };
}


function executeStats() {
    const targetUrl = STATS_URL + "?" + getQueryParamsStr();
    
    document.getElementById("express-status").innerHTML = "Please wait...";
    document.getElementById("express-report").innerHTML = "";
    document.getElementById("execute-express-button").style.display = "none";
    document.getElementById("express-loading").style.display = "inline-block";
    
    d3.dsv(",", targetUrl, convertRow).then(
        updateReport,
        (x) => alert("Failed to pull data.")
    );
}


function setupExpress() {
    document.getElementById("express-loading").style.display = "none";
    document.getElementById("execute-express-button").addEventListener("click", (event) => {
        const dimension = document.getElementById("dimension-select").value;
        
        if (isAll(dimension)) {
            executeExport();
        } else {
            executeStats();
        }

        event.preventDefault();
    });
}


setupExpress();
