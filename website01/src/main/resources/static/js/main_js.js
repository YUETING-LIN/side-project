var app = window.AddressSeleclList = {
    AddressArray: [
        ['基隆市', '仁愛區', '信義區', '中正區', '中山區', '安樂區', '暖暖區', '七堵區'],
        ['台北市', '中正區', '大同區', '中山區', '松山區', '大安區', '萬華區', '信義區', '士林區', '北投區', '內湖區', '南港區', '文山區'],
        ['新北市', '板橋區', '中和區', '永和區', '土城區', '三峽區', '鶯歌區', '樹林區', '新莊區', '三重區', '蘆洲區', '五股區', '泰山區', '林口區', '八里區', '淡水區', '三芝區', '石門區', '金山區', '萬里區', '汐止區', '瑞芳區', '貢寮區', '平溪區', '雙溪區', '新店區', '深坑區', '石碇區', '坪林區', '烏來區'],
        ['桃園市', '桃園區', '龜山區', '八德區', '大溪區', '蘆竹區', '大園區', '中壢區', '龍潭區', '平鎮區', '楊梅區', '新屋區', '觀音區', '復興區'],
        ['新竹縣', '竹北市', '新埔鎮', '竹東鎮', '關西鎮', '寶山鄉', '湖口鄉', '新豐鄉', '芎林鄉', '五峰鄉', '橫山鄉', '尖石鄉', '北埔鄉', '峨眉鄉'],
        ['新竹市', '北區', '東區', '香山區'],
        ['苗栗縣', '頭份市', '苗栗市', '竹南鎮', '後龍鎮', '通霄鎮', '苑裡鎮', '卓蘭鎮', '三灣鄉', '南庄鄉', '獅潭鄉', '造橋鄉', '頭屋鄉', '公館鄉', '大湖鄉', '泰安鄉', '銅鑼鄉', '三義鄉', '西湖鄉'],
        ['台中市', '中區', '東區', '南區', '西區', '北區', '北屯區', '西屯區', '南屯區', '太平區', '大里區', '霧峰區', '烏日區', '豐原區', '后里區', '石岡區', '東勢區', '和平區', '新社區', '潭子區', '大雅區', '神岡區', '大肚區', '沙鹿區', '龍井區', '梧棲區', '清水區', '大甲區', '外埔區', '大安區'],
        ['彰化縣', '彰化市', '員林市', '鹿港鎮', '和美鎮', '溪湖鎮', '田中鎮', '北斗鎮', '二林鎮', '花壇鄉', '秀水鄉', '芬園鄉', '福興鄉', '線西鄉', '伸港鄉', '社頭鄉', '永靖鄉', '埔心鄉', '大村鄉', '埔鹽鄉', '田尾鄉', '埤頭鄉', '溪州鄉', '竹塘鄉', '大城鄉', '芳苑鄉', '二水鄉'],
        ['南投縣', '南投市', '草屯鎮', '埔里鎮', '集集鎮', '竹山鎮', '中寮鄉', '國姓鄉', '仁愛鄉', '名間鄉', '水里鄉', '魚池鄉', '信義鄉', '鹿谷鄉'],
        ['雲林縣', '斗六市', '斗南鎮', '虎尾鎮', '土庫鎮', '西螺鎮', '北港鎮', '大埤鄉', '褒忠鄉', '東勢鄉', '台西鄉', '崙背鄉', '麥寮鄉', '林內鄉', '古坑鄉', '莿桐鄉', '二崙鄉', '水林鄉', '口湖鄉', '四湖鄉', '元長鄉'],
        ['嘉義市', '西區', '東區'],
        ['嘉義縣', '太保市', '朴子市', '大林鎮', '布袋鎮', '番路鄉', '梅山鄉', '竹崎鄉', '阿里山鄉', '中埔鄉', '大埔鄉', '水上鄉', '鹿草鄉', '東石鄉', '六腳鄉', '新港鄉', '民雄鄉', '溪口鄉', '義竹鄉'],
        ['台南市', '中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '仁德區', '關廟區', '龍崎區', '新營區', '鹽水區', '柳營區', '後壁區', '白河區', '東山區', '佳里區', '學甲區', '北門區', '將軍區', '西港區', '七股區', '官田區', '麻豆區', '大內區', '六甲區', '下營區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '善化區', '新市區', '山上區', '安定區'],
        ['高雄市', '新興區', '前金區', '苓雅區', '鹽埕區', '鼓山區', '旗津區', '前鎮區', '三民區', '楠梓區', '小港區', '左營區', '仁武區', '大社區', '岡山區', '路竹區', '阿蓮區', '田寮區', '燕巢區', '橋頭區', '梓官區', '彌陀區', '永安區', '湖內區', '鳳山區', '大寮區', '林園區', '鳥松區', '大樹區', '旗山區', '美濃區', '六龜區', '內門區', '杉林區', '甲仙區', '桃源區', '那瑪夏區', '茂林區', '茄萣區'],
        ['屏東縣', '屏東市', '潮州鎮', '恆春鎮', '東港鎮', '三地門鄉', '霧台鄉', '瑪家鄉', '九如鄉', '里港鄉', '高樹鄉', '鹽埔鄉', '長治鄉', '麟洛鄉', '竹田鄉', '內埔鄉', '萬丹鄉', '泰武鄉', '來義鄉', '萬巒鄉', '崁頂鄉', '新埤鄉', '南州鄉', '林邊鄉', '琉球鄉', '佳冬鄉', '新園鄉', '枋寮鄉', '枋山鄉', '春日鄉', '獅子鄉', '車城鄉', '牡丹鄉', '滿州鄉'],
        ['宜蘭縣', '宜蘭市', '頭城鎮', '羅東鎮', '蘇澳鎮', '礁溪鄉', '壯圍鄉', '員山鄉', '三星鄉', '大同鄉', '五結鄉', '冬山鄉', '南澳鄉'],
        ['花蓮縣', '花蓮市', '鳳林鎮', '新城鄉', '玉里鎮', '秀林鄉', '吉安鄉', '壽豐鄉', '光復鄉', '豐濱鄉', '瑞穗鄉', '萬榮鄉', '卓溪鄉', '富里鄉'],
        ['台東縣', '台東市', '關山鎮', '成功鎮', '綠島鄉', '蘭嶼鄉', '延平鄉', '卑南鄉', '鹿野鄉', '海端鄉', '池上鄉', '東河鄉', '長濱鄉', '太麻里鄉', '金峰鄉', '大武鄉', '達仁鄉'],
        ['澎湖縣', '馬公市', '西嶼鄉', '望安鄉', '七美鄉', '白沙鄉', '湖西鄉'],
        ['金門縣', '金沙鎮', '金湖鎮', '金寧鄉', '金城鎮', '烈嶼鄉', '烏坵鄉'],
        ['連江縣', '南竿鄉', '北竿鄉', '莒光鄉', '東引鄉'],
    ],

    defaultOptionCityText: '選縣市',
    defaultOptionCityValue: '',
    defaultOptionAreaText: '選鄉鎮',
    defaultOptionAreaValue: '',

    Initialize: function(city, area, defaultCityText, defaultCityValue, defaultAreaText, defaultAreaValue) {

        var cityText = defaultCityText ? defaultCityText : this.defaultOptionCityText;
        var cityValue = defaultAreaValue ? defaultAreaValue : this.defaultOptionCityValue;
        var areaText = defaultAreaText ? defaultAreaText : this.defaultOptionAreaText;
        var areaValue = defaultAreaValue ? defaultAreaValue : this.defaultOptionAreaValue;

        var citySelect = document.getElementById(city);
        var areaSelect = document.getElementById(area);

        citySelect.options[0] = new Option(cityText, cityValue);
        areaSelect.options[0] = new Option(areaText, areaValue);
        for (var i = 0; i < this.AddressArray.length; i++) {
            citySelect.options[i + 1] = new Option(this.AddressArray[i][0], this.AddressArray[i][0]);
        }
        citySelect.addEventListener ? citySelect.addEventListener('change', function(e) { app.AppendArea(e, areaSelect, areaText, areaValue) }, false) : citySelect.attachEvent('onchange', function(e) { app.AppendArea(e, areaSelect, areaText, areaValue) });
    },

    AppendArea: function(e, AreaSelect, areaText, areaValue) {
        var target = e.target ? e.target : e.srcElement;
        if (target.selectedIndex == 0) {
            AreaSelect.options.length = 0;
            AreaSelect.options[0] = new Option(areaText, areaValue);
            return;
        }
        AreaSelect.options.length = this.AddressArray[target.selectedIndex - 1].length - 1;
        for (var i = 1; i < this.AddressArray[target.selectedIndex - 1].length; i++) {
            AreaSelect.options[i - 1] = new Option(this.AddressArray[target.selectedIndex - 1][i], this.AddressArray[target.selectedIndex - 1][i]);
        }
    },

    ReturnSelectAddress: function(city, area) {
        var county = document.getElementById(city);
        var area = document.getElementById(area);
        return "用餐地點: " + county.value + area.value;
    }
};

window.onload = function() {
    //當頁面載完之後，用AddressSeleclList.Initialize()，
    //傳入要綁定的縣市下拉選單ID及鄉鎮市區下拉選單ID
    AddressSeleclList.Initialize('縣市1', '鄉鎮市區1');
    //後面四個參數分別是兩個下拉選單的預設文字跟值
    //AddressSeleclList.Initialize('縣市2', '鄉鎮市區2', 'Please Select City', '0', 'Please Select Area', '0');
    var changeSingleItem = document.getElementById("time");
    var innerSingleItem = "";
    var SingleItemData = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30'];
    for (var i = 0; i < SingleItemData.length; i++) {
        innerSingleItem = innerSingleItem + '<option value=\"' + SingleItemData[i] + '\">' + SingleItemData[i] + '</option>';
    }
    changeSingleItem.innerHTML = innerSingleItem;
    //自動建立用餐時間
}



function week() {
    //取出用餐時間值
    var w = $('select[name="week"]').val();
    return w;
}

function time() {
    //取出用餐時間值
    var t = $('select[name="time"]').val();
    return t;
}


function price() {
    //取出用餐金額值
    var minp = $('input[name="minp"]').val();
    var maxp = $('input[name="maxp"]').val();
    return minp + "~" + maxp;

}

function show() {

    //取出指定縣市及鄉鎮市區的下拉選單的值
    var data1 = "\n用餐時間: " + week() + "　" + time();
    //var data2="\n用餐金額: "+price()+"元";
    confirm(AddressSeleclList.ReturnSelectAddress('縣市1', '鄉鎮市區1') + data1);
    //計算搜尋次數
    /* var count =parseInt(document.getElementById("button-count").innerHTML)-1;
     console.log(count);
     if(count==0){
         document.getElementById("button-count").innerHTML=count;//歸零後禁止使用
         document.getElementById("button-search").setAttribute('disabled','true');
     }else{
         document.getElementById("button-count").innerHTML=count;
     }*/
}