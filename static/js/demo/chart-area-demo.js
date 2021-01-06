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
  var project_id = document.getElementById("project_id").value
  get_project_chart(project_id)
  set_card(project_id)
  get_project_pie(project_id)
  
}

$(document).ready(function () {
  get_project_chart(0)
  set_card(0)
  get_project_pie(0)
});

function set_card(project_id) {
  
  $.ajax({
    url: '/manager/card/' + project_id,
    type: 'GET',
    dataType: 'json',
    success: (data) => {

      $('#openTickets').html(JSON.stringify(data.openTickets))
      $('#unassignedTickets').html(JSON.stringify(data.unassignedTickets))
      $('#assignedTickets').html(JSON.stringify(data.assignedTickets))
      if (data.timePerTicket != null)
        $('#timePerTicket').html(JSON.stringify(data.timePerTicket))
      else
      $('#timePerTicket').html('-')

      $('#unassignedTicketsDiv').remove()
      style_width = (data.unassignedTickets / data.openTickets) * 100;
      var div = '<div id="unassignedTicketsDiv" class="progress-bar bg-warning" style="width:'+style_width +'%" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>'
      $('#unassignedup').append(div);
      

      $('#assignedTicketsDiv').remove()
      style_width = (data.assignedTickets / data.openTickets) * 100;
      var div2 = '<div id="assignedTicketsDiv" class="progress-bar bg-info" style="width:'+style_width +'%" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>'
      $('#assignedup').append(div2);
      

      
    }
  });
}

function get_project_pie(project_id) {
  $.ajax({
    url: '/manager/pie-chart/'+ project_id,
    type: 'GET',
    dataType: 'json',
    success: (back_data) => {
      var datalabels = []
      var datasets = []

      for ( i = 0; i < 3; i++){
        datalabels.push(back_data[i].priority)
        datasets.push(back_data[i].cnt)
      }
      $('#myPieChart').remove();
      $('#pie-area').append('<canvas id="myPieChart"><canvas>');
      var ctx = document.getElementById("myPieChart");
      var myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: datalabels,
          datasets: [{
            data: datasets,
            backgroundColor: ['#1cc88a', '#4e73df', '#36b9cc'],
            hoverBackgroundColor: ['#17a673', '#2e59d9', '#2c9faf'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
          }],
        },
        options: {
          maintainAspectRatio: false,
          tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
          },
          legend: {
            display: true,
            position: 'right'
          },
          cutoutPercentage: 75,
        },
      });
    }
  })
}

function get_project_chart(project_id) {
  $.ajax({
    url: '/manager/chart/'+ project_id,
    type: 'GET',
    dataType: 'json',
    success: (back_data) => {
      var datasets = [];
      var month_name = [];
      var month_count = 0;
      var array_color = ["#b2b266", "#4e73df", "#ff6666", "#d2ff4d", "#ffbb33", "#adad85"];
      for (var proj_count = 0; proj_count < back_data.totalProjects; proj_count++){
        var datalabels = []
        for (var i = 0; i < back_data.chart_data.length; i++) {
          if (back_data.chart_data[i].p_id == back_data.project[proj_count].p_id) {
            datalabels.push(back_data.chart_data[i].cnt)
            if (proj_count == 0) {
              month_name.push(back_data.chart_data[i].month)
            }
            color_dark = array_color[proj_count]
            month_count++;
            var some = {
              label: back_data.chart_data[i].name,
              lineTension: 0.3,
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
          }
          if (month_count == 12) {
            datasets.push(some)
            console.log(i)
            console.log(back_data.chart_data[i])
            console.log(some.label)
            month_count = 0
          }
          
        }
      }
      $('#myAreaChart').remove();
      $('#chart-area').append('<canvas id="myAreaChart"><canvas>');
      var ctx = document.getElementById("myAreaChart");
      var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: month_name,
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
            position: 'right'
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