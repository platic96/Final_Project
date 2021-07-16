function getUpbitData(market, count, tag) {
    var upbitData;
    $.ajax({
        url:'/candle',
        type:'POST',
        data: JSON.stringify({'market': market}),
        async:false,
        dataType:'json',
        contentType: 'application/json',
        success:function(data){
            upbitData = JSON.parse(JSON.stringify(data));
        }
    })
    var candleCharData = [];

     for(var i=0; i<upbitData.length; i++) {
      let tmp = [upbitData[i].low_price, upbitData[i].opening_price, upbitData[i].trade_price, upbitData[i].high_price]
      tmp.unshift(upbitData[i].candle_date_time_kst.split('T')[1])
      candleCharData.push(tmp)
    }

  candleCharData.reverse()

  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {
    var data = google.visualization.arrayToDataTable(candleCharData, true);

    var options = {
      legend: 'none',
      bar: { groupWidth: '100%' }, // Remove space between bars.
      candlestick: {
        fallingColor: { strokeWidth: 0, fill: '#a52714' }, // red
        risingColor: { strokeWidth: 0, fill: '#0f9d58' }   // green
      }
    };

    var chart = new google.visualization.CandlestickChart(tag);
    chart.draw(data, options);
  }
}
