document.addEventListener("DOMContentLoaded", function () {
  var plotForm = document.getElementById("plotForm");
  var plotContainer = document.getElementById("plotContainer");
  var loader = document.querySelector(".loader");

  plotForm.addEventListener("submit", function (e) {
    e.preventDefault();
  });

  var beginDate = document.getElementById("begin").value;
  var endDate = document.getElementById("end").value;

  if (!beginDate || !endDate || beginDate > endDate) {
    alert("please select valid date range");
    return;
  }

  var today = new Date().toISOString().split("T")[0];

  if (beginDate > today || endDate > today) {
    alert("Selected dates should be from past/present but not future");
    return;
  }
});
