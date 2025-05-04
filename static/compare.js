document.addEventListener("DOMContentLoaded", function () {
  var compareForm = document.getElementById("compareForm");
  var plotContainer = document.getElementById("plotContainer");
  var loader = document.querySelector(".loader");

  compareForm.addEventListener("submit", function (e) {
    e.preventDefault();

    var selectedStocks = Array.from(
      document.getElementById("stocks").selectedOptions
    ).map((option) => option.value);

    // first check if dates are selected correctly
    var beginDate = document.getElementById("begin").value;
    var endDate = document.getElementById("end").value;

    if (!beginDate || !endDate || beginDate > endDate) {
      alert("Please select valid date range.");
      return;
    }

    // Check if dates are before today's date
    var today = new Date().toISOString().split("T")[0];

    if (beginDate > today || endDate > today) {
      alert("Selected dates should be from past/present, not future.");
      return;
    }
    
    var requestData = {
      stocks: selectedStocks,
      begin: document.getElementById("begin").value,
      end: document.getElementById("end").value,
      criteria: document.getElementById("criteria").value,
    };

    // create a post fetch request to the server

    // Show loader
    loader.style.display = "block";

    fetch("/api/compare", {
      method: "POST",
      body: JSON.stringify(requestData),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json(); // Parse the response as JSON and return the promise
      })
      .then(function (jsonData) {
        console.log("JSON Data from server:", jsonData);

        var iFrameElement = document.createElement("iframe");
        iFrameElement.src = jsonData.image_path;

        iFrameElement.style.width = "70vw";
        iFrameElement.style.height = "68vh";

        // Hide loader
        loader.style.display = "none";

        plotContainer.innerHTML = "";
        plotContainer.appendChild(iFrameElement);
      })
      .catch(function (error) {
        // Hide loader in case of an error
        loader.style.display = "none";
        console.error("Fetch error:", error);
      });
  });
});
