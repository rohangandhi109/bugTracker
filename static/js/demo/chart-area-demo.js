// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

function change_project() {
  get_project(document.getElementById("project_id").value)
}

$(document).ready(function () {
  get_project(0)
});

function get_project(project_id) {
  $.ajax({
    url: 'http://127.0.0.1:5000/manager/chart/'+ project_id,
    type: 'GET',
    dataType: 'json',
    success: (back_data) => {
      var color1 = 48
      var color2 = 10
      var color3 = 28
      var datasets = [];
      var increment = 255/back_data.totalProjects 
      var j = 0;
      for (i = 0; i < back_data.totalProjects; i++) { 
        var datalabels = []
        for (j = j; j < (12 + ( 12 * i))  ; j++) {
          datalabels.push(back_data.chart_data[j].cnt)
        }
        color1 += (i * increment)
        color2 += (i * increment)
        color3 += (i * increment)
        color_light = "rgba(" + color1 + "," + color2 + "," + color3 + ", 0)";
        color_dark = "rgba(" + color1 + "," + color2 + "," + color3 + ", 1)";
        var some = {
          label: back_data.chart_data[j-1].name,
          lineTension: 0.3,
          backgroundColor: color_light,
          borderColor: color_dark,
          pointRadius: 3,
          pointBackgroundColor: color_dark,
          pointBorderColor: color_dark,
          pointHoverRadius: 3,
          pointHoverBackgroundColor: color_dark,
          pointHoverBorderColor: color_dark,
          pointHitRadius: 10,
          pointBorderWidth: 2,
          data: datalabels
        }
        datasets.push(some)
      }
      $('#myAreaChart').remove();
      $('#chart-area').append('<canvas id="myAreaChart"><canvas>');
      var ctx = document.getElementById("myAreaChart");
      var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ["Jan", "Feb", "Mar", "Apr", "May", "jun", "jul", "aug", "sep", "oct", "nov", "dec"],
          datasets: datasets,
        },
        options: {
          maintainAspectRatio: false,
          layout: {
            padding: {
              left: 10,
              right: 25,
              top: 25,
              bottom: 0
            }
          },
          scales: {
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Month'
              },
              time: {
                unit: 'date'
              },
              gridLines: {
                display: false,
                drawBorder: false
              },
              ticks: {
                maxTicksLimit: 12
              }
            }],
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Tickets'
              },
              ticks: {
                maxTicksLimit: 7,
                stepSize: 2,
                padding: 10,
                // Include a dollar sign in the ticks
                callback: function (value, index, values) {
                  return  number_format(value);
                }
              },
              gridLines: {
                color: "rgb(234, 236, 244)",
                zeroLineColor: "rgb(234, 236, 244)",
                drawBorder: false,
                borderDash: [2],
                zeroLineBorderDash: [2]
              }
            }],
          },
          legend: {
            display: true,
            position: 'bottom'
          },
          tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            titleMarginBottom: 10,
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            intersect: false,
            mode: 'index',
            caretPadding: 10,
            callbacks: {
              label: function (tooltipItem, chart) {
                var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                return datasetLabel + ':' + number_format(tooltipItem.yLabel);
              }
            }
          }
        }
      });

    }
  })
}