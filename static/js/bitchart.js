function change(){
  setUpbitData()
}

function change_select(tickers,sort) {
  tickers.sort((a, b) => {
    if (sort == "ko_name") {
      if (a.ko_name > b.ko_name) {
        return 1
      }
      if (a.ko_name < b.ko_name) {
        return -1
      }
      return 0
    }
    else if (sort == "now") {
      if (a.trade_price > b.trade_price) {
        return 1
      }
      if (a.trade_price < b.trade_price) {
        return -1
      }
      return 0
    }
    else if (sort == "yesterday") {
      if (a.signed_change_rate > b.signed_change_rate) {
        return 1
      }
      if (a.signed_change_rate < b.signed_change_rate) {
        return -1
      }
      return 0
    }
    else if (sort == "money") {
      if (a.acc_trade_price_24h > b.acc_trade_price_24h) {
        return 1
      }
      if (a.acc_trade_price_24h < b.acc_trade_price_24h) {
        return -1
      }
      return 0
    }
  })
  console.log(tickers)
  return tickers
}
function connection(ticker, markets) {
  for (i = 0; i < markets.length; i++) {
    for (j = 0; j < ticker.length; j++) {
      if (ticker[j].market == markets[i].market)
        ticker[j].ko_name = markets[i].korean_name;
    }
  }
  return ticker
}
function comma(str) {
  str = String(str);
  return str.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
}
function setUpbitData() {
  $.ajax({
    url: "https://api.upbit.com/v1/market/all",
    dataType: "json"
  }).done(function (markets) {
    //$("#tmp").html( JSON.stringify(markets) );
    let arr_krw_markets = "";
    let arr_korean_name = [];

    for (var i = 0; i < markets.length; i++) {
      if (markets[i].market.indexOf("KRW") > -1) {
        arr_krw_markets += markets[i].market + (",");
      }
    }
    arr_krw_markets = arr_krw_markets.substring(0, arr_krw_markets.length - 1);
    //$("#tmp").html( arr_krw_markets );
    $.ajax({
      url: "https://api.upbit.com/v1/ticker?markets=" + arr_krw_markets,
      dataType: "json"
    }).done(function (tickers) {
      //console.log(tickers)
      tikers = connection(tickers, markets)
      var option = $("#sort option:selected").val();
      tikers=change_select(tickers,option)
      //tickers = change_select(tickers, selectOption)
      $("#table_ticker > tbody > tr").remove();
      //alert($("#table_ticker > tbody > tr").length);
      $("#table_ticker").fadeOut("slow");
      for (let i = 0; i < tickers.length; i++) {
        let rowHtml = "<tr onClick =\"location.href='/bitdetail?market="+tickers[i].market+"&openprice="+tickers[i].opening_price+"&highprice="+tickers[i].high_price+"&lowprice="+tickers[i].low_price+"&tradeprice="+tickers[i].trade_price+"'\"><td>" 
        rowHtml += "<td>" + tickers[i].ko_name+"</td>"
        rowHtml += "<td>" + comma(tickers[i].trade_price) + "</td>"
        rowHtml += "<td>" + comma((tickers[i].signed_change_rate * 100).toFixed(2)) + " %" + "</td>"
        rowHtml += "<td>" + comma((tickers[i].acc_trade_price_24h > 1000000 ? (tickers[i].acc_trade_price_24h / 1000000) : tickers[i].acc_trade_price_24h).toFixed(0)) + (tickers[i].acc_trade_price_24h > 1000000 ? "백만" : "") + "</td>"
        rowHtml += "</tr>";
        $("#table_ticker > tbody:last").append(rowHtml);
        //markets[i].korean_name
      } // end for...
      $("#table_ticker").fadeIn("slow");
    })  //done(function(tickers){
  }) // end done(function(markets){
    .fail(function () {
      //alert("업비트 API 접근 중 에러.")}
      $("#tmp").text("API 접근 중 에러.");
    })
  setTimeout(setUpbitData, 13000);
}
$(function () {
  setUpbitData();
});