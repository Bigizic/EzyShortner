drawBarChart([ 1, 2, 3, 4, 5 ], {}, $("#basic"));

drawBarChart([ 1, 2, 3, 4, 5 ], {
  title: "Dunder Mifflin&mdash;Quabity Assuance Over Time",
  height: "500px",
  width: "800px",
  barSpacing: "5%",
  barColor: "#ace",
  showTicks: true,
  yAxisName: "Blunders (per month)"
}, $("#options"));

drawBarChart({
  "Northwest": { "Qtr 1": 3767341, "Qtr 2": 3298694, "Qtr 3": 2448772, "Qtr 4": 1814281 },
  "Northeast": { "Qtr 1": 2857163, "Qtr 2": 3607148, "Qtr 3": 1857156, "Qtr 4": 1983931 },
  "Central": { "Qtr 1": 3677108, "Qtr 2": 3205014, "Qtr 3": 2390120, "Qtr 4": 1762757 },
  "Southwest": { "Qtr 1": 2851432, "Qtr 2": 3571335, "Qtr 3": 1932932, "Qtr 4": 1653192 }
}, {
  title: "Sales by Division and by Quarter&mdash;2018",
  width: "550px",
  height: "400px",
  yAxisName: "Dollars (CAD)",
  xAxisName: "Division",
  showTicks: true,
  barSpacing: "10px",
  barColor: [ "#ace", "#eac", "#cea", "#cae" ],
  legendPosition: { bottom: "50px", right: "-60px" }
}, $("#stacked-extra"));

drawBarChart({
  "Sunday": { "Apples": 1, "Oranges": 1, "Bananas": 2 },
  "Monday": { "Apples": 1, "Oranges": 2, "Bananas": 3 },
  "Tuesday": { "Apples": 2, "Oranges": 3, "Bananas": 5 },
  "Wednesday": { "Apples": 3, "Oranges": 5, "Bananas": 8 },
  "Thursday": { "Apples": 5, "Oranges": 8, "Bananas": 13 },
  "Friday": { "Apples": 8, "Oranges": 13, "Bananas": 21 },
  "Saturday": { "Apples": 13, "Oranges": 21, "Bananas": 34 }
}, {
  title: "Fibbonaci's Fruit",
  width: "800px",
  height: "500px",
  barSpacing: "20px",
  barColor: [ "#f00", "#f90", "#ff0" ],
  valueLabelColor: "#555",
  legendPosition: { bottom: "250px", left: "300px" }
}, $("#fibb"));
