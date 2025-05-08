document.addEventListener("DOMContentLoaded", function () {
  var plotForm = document.getElementById("plotForm");
  var plotContainer = document.getElementById("plotContainer");
  var loader = document.querySelector(".loader");

  plotForm.addEventListener("submit", function (e) {
    e.preventDefault();

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
      stock: document.getElementById("stock").value,
      begin: document.getElementById("begin").value,
      end: document.getElementById("end").value,
      criteria: document.getElementById("criteria").value,
    };

    var params = new URLSearchParams(requestData);

    // Show loader
    loader.style.display = "block";

    // create a fetch request to the server
    fetch("/api/plot?" + params, {
      method: "GET",
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
        iFrameElement.style.height = "70vh";

        // Hide loader
        loader.style.display = "none";

        plotContainer.innerHTML = "";
        plotContainer.appendChild(iFrameElement);
        // Now you can use jsonData as needed in your application
      })
      .catch(function (error) {
        // Hide loader in case of an error
        loader.style.display = "none";
        console.error("Fetch error:", error);
      });
  });
});
