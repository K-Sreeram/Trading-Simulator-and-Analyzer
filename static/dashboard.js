function renderTable(data) {
  var table = document.getElementById("dataTable");
  var orderBy = document.getElementById("orderBy");

  table.innerHTML = "";

  var thread = table.createThread();
  var row = thread.insertRow();
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

    var loader = document.getElementsByClassName("loader")[0];
    loader.style.display = "none";
  }
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
  }, 1000);
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
