$('select').change(function () {
  $.getJSON("/refresh", {
      over_date: $(this).closest('.tab-pane').find("select[name='over_date']").val() || '30+',
      amount: $(this).closest('.tab-pane').find("select[name='amount']").val(),
    }, function (data, textStatus, jqXHR) {
      if ($(this).closest('.tab-pane').is('.vintage')) {
        refresh_vintage(data)
      }else{
        refresh_rate(data.rates);
      }
    }.bind(this)
  );
});
$('.tab-pane').find('select:first').change();

function refresh_vintage(data) {
  Highcharts.chart('container', {

    title: {
      text: 'Vintage analysis max overdue',
    },

    xAxis: {
      categories: data.vintages.categories
    },

    yAxis: {
      labels: {
        format: '{value} %',
      },
      title: {
        text: 'rate'
      },
      max: 100
    },
    tooltip: {
      headerFormat: '<span style="font-size: 10px"><b>Month</b> {point.key}</span><br/>',
      valueDecimals: 2,
      valueSuffix: ' %'
    },

    credits: {
      enabled: false
    },

    series: data.vintages.data
  });
  Highcharts.chart('container0', {

    title: {
      text: 'Vintage analysis current overdue',
    },

    xAxis: {
      categories: data.vintage_currents.categories
    },

    yAxis: {
      labels: {
        format: '{value} %',
      },
      title: {
        text: 'rate'
      },
      max: 100
    },
    tooltip: {
      headerFormat: '<span style="font-size: 10px"><b>Month</b> {point.key}</span><br/>',
      valueDecimals: 2,
      valueSuffix: ' %'
    },

    credits: {
      enabled: false
    },

    series: data.vintage_currents.data
  });
}

function refresh_rate(data) {
  Highcharts.chart('container1', {
    chart: {
      // type: 'column'
    },

    title: {
      text: 'Amount and rate'
    },

    xAxis: {
      categories: data.categories
    },
    yAxis: [{ // Primary yAxis
      labels: {
        format: '{value} %',
      },
      title: {
        text: 'percent',
      },
      opposite: true,
      max: 100
    }, { // Secondary yAxis
      gridLineWidth: 0,
      title: {
        text: 'num',
      },
      labels: {
        format: '{value}',
      }

    }],

    credits: {
      enabled: false
    },

    series: [{
      name: '通过率',
      type: 'spline',
      data: data.data['通过率'],
      marker: {
        enabled: false
      },
      tooltip: {
        valueSuffix: ' %',
        valueDecimals: 2,
      }

    }, {
      name: '撤单率',
      type: 'spline',
      data: data.data['撤单率'],
      marker: {
        enabled: false
      },
      dashStyle: 'shortdot',
      tooltip: {
        valueSuffix: ' %',
        valueDecimals: 2,
      }

    }, {
      name: '注册率',
      type: 'spline',
      data: data.data['注册率'],
      marker: {
        enabled: false
      },
      dashStyle: 'shortdot',
      tooltip: {
        valueSuffix: ' %',
        valueDecimals: 2,
      }

    }, {
      name: '有效单',
      type: 'column',
      yAxis: 1,
      data: data.data['有效单'],
      dashStyle: 'shortdot',
      tooltip: {
      }

    }, {
      name: '通过单',
      type: 'column',
      yAxis: 1,
      data: data.data['通过单'],
      dashStyle: 'shortdot',
      tooltip: {
      }

    }]
  });
  Highcharts.chart('container2', {
    chart: {
      type: 'column'
    },

    title: {
      text: 'Money'
    },

    xAxis: {
      categories: data.categories
    },
    yAxis: {
      title: {
        text: ''
      },
    },
    tooltip: {
    },

    credits: {
      enabled: false
    },

    series: [{
      name: '注册金',
      data: data.data['注册金']
    }]
  });
}

Highcharts.chart('container3', {
  chart: {
    type: 'column'
  },

  title: {
    text: '注册单量大于100的金额的分布'
  },

  xAxis: {
    categories: ['1500', '2000', '2500', '3000', '4000', '5000', '6000', '7000', '8000', '9000', '10000', '11000', '13000', '15000', '20000', '30000']
  },
  yAxis: {
    title: {
      text: ''
    },
  },
  tooltip: {
  },

  credits: {
    enabled: false
  },

  series: [{
    name: '单数',
    data: [1345, 39086, 341, 46165, 29929, 60172, 22132, 4492, 15537, 17061, 69089, 158, 921, 205, 3640, 3591]
  }]
});