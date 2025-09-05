/**
 * Logic for running the express version.
 * 
 * @license BSD
 */

const EXPORT_URL = "https://6saet4fqci.execute-api.us-east-2.amazonaws.com/default/gafj-topic-explorer-export";
const STATS_URL = "https://g69mcjf2re.execute-api.us-east-2.amazonaws.com/default/gafj-topic-explorer-stat";


/**
 * Determine if a value refers to all / no filter value.
 * 
 * @param target The string selected or provided by the user.
 * @return True if interpreted as no filter and false otherwise.
 */
function isAll(target) {
    return target === "all" || target === "All" || target === "";
}


/**
 * Get a parameter for a user defined query.
 * 
 * @param elementId The ID of the input element from which to get a user defined query parameter.
 * @return Object with name of query parameter and query parameter value.
 */
function getQueryParam(elementId) {
    const name = elementId.split("-")[0];
    const value = document.getElementById(elementId).value;
    return {"name": name, "value": value};
}


/**
 * Get a URL query parameter string from the query defined by the user.
 * 
 * @return URL appendable string describing the user defined query.
 */
function getQueryParamsStr() {
    const elements = [
        getQueryParam("country-select"),
        getQueryParam("category-select"),
        getQueryParam("tag-select"),
        getQueryParam("keyword-input"),
        getQueryParam("dimension-select")
    ];

    const validElementsWithBlank = elements.filter((x) => !isAll(x["value"]));
    const validElements = validElementsWithBlank.filter((x) => x !== "");
    const elementStrs = validElements.map((x) => x["name"] + "=" + encodeURIComponent(x["value"]));
    return elementStrs.join("&");
}


/**
 * Request a CSV export by opening a new tab using a URL defined by the user's query.
 */
function executeExport() {
    const queryParamsStr = getQueryParamsStr();
    if (queryParamsStr === "") {
        window.open("/csv/articles.csv", "_blank");
    } else {
        const targetUrl = EXPORT_URL + "?" + queryParamsStr;
        window.open(targetUrl, "_blank");
    }
}


/**
 * Update the express report visualization table.
 * 
 * @param rows The records to show in the visualization table (Array of Object).
 */
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

    // Status updates removed - using loading indicator instead
    document.getElementById("execute-express-button").style.display = "inline-block";
    document.getElementById("express-loading").style.display = "none";
}


/**
 * Parse a raw row returned by the express API service.
 * 
 * @param rawRow The raw row returned by the server.
 * @return The row but with its values interpreted and cast.
 */
function convertRow(rawRow) {
    return {
        "name": rawRow["name"],
        "percent": parseFloat(rawRow["percent"]) * 100
    };
}


/**
 * Execute a request for article aggregate stats using the user's currently defined query.
 */
function executeStats() {
    const targetUrl = STATS_URL + "?" + getQueryParamsStr();
    
    // Show loading indicator
    document.getElementById("express-report").innerHTML = "";
    document.getElementById("execute-express-button").style.display = "none";
    document.getElementById("express-loading").style.display = "inline-block";
    
    d3.dsv(",", targetUrl, convertRow).then(
        updateReport,
        (x) => alert("Failed to pull data.")
    );
}


/**
 * Prepare the express visualization including event listeners.
 */
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
