// Get data from local storage if it exists
var cachedData = sessionStorage.getItem("cachedLiveData");

// If data exists, render table with it else fetch data from server
if (cachedData) {
  cachedData = JSON.parse(cachedData);
  renderTable(cachedData);
} else {
  fetchData();
}

function fetchData() {
  fetch("/api/liveData", {
    method: "GET",
  })
    .then(function (response) {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then(function (jsonData) {
      jsonData = Object.values(jsonData);
      var data = jsonData;

      // Cache data in local storage
      sessionStorage.setItem("cachedLiveData", JSON.stringify(data));

      // Render table with data
      renderTable(data);
    })
    .catch(function (error) {
      console.error("Error:", error);
    });
}

function renderTable(data) {
  var table = document.getElementById("dataTable");
  var orderBy = document.getElementById("orderBy");

  // Clear existing table content
  table.innerHTML = "";

  // Create table header row
  var thead = table.createTHead();
  var row = thead.insertRow();
  columns = Object.keys(data[0]);
  for (var key of columns) {
    let th = document.createElement("th");
    let text = document.createTextNode(key);
    th.appendChild(text);
    row.appendChild(th);
  }

  for (var element of data) {
    var row = table.insertRow();
    for (key in element) {
      var cell = row.insertCell();
      var text = document.createTextNode(element[key]);
      cell.appendChild(text);
    }
  }

  var loader = document.getElementsByClassName("loader")[0];
  loader.style.display = "none";
}

function orderBy(property) {
  return function (a, b) {
    if (a[property] > b[property]) {
      return 1;
    } else if (a[property] < b[property]) {
      return -1;
    } else {
      return 0;
    }
  };
}

function sortData() {
  var orderBySelector = document.getElementById("orderBy");
  var selectedProperty = orderBySelector.value;

  var loader = document.getElementsByClassName("loader")[0];
  loader.style.display = "block";

  setTimeout(function () {
    cachedData.sort(orderBy(selectedProperty));
    cachedData.reverse();
    renderTable(cachedData);
    loader.style.display = "none";
  }, 1000); // Simulating an asynchronous operation with a timeout
}

function filterData() {
  var filterBySelector = document.getElementById("filterBy");
  var selectedProperty = filterBySelector.value;

  var filterFrom = document.getElementById("filterFrom");
  var filterTo = document.getElementById("filterTo");

  var filterFromValue = parseFloat(filterFrom.value);
  var filterToValue = parseFloat(filterTo.value);

  var loader = document.getElementsByClassName("loader")[0];
  loader.style.display = "block";

  setTimeout(function () {
    data = cachedData.filter(function (item) {
      var itemValue = parseFloat(item[selectedProperty]);
      return itemValue >= filterFromValue && itemValue <= filterToValue;
    });
    renderTable(data);
    loader.style.display = "none";
  }, 1000); // Simulating an asynchronous operation with a timeout
}
