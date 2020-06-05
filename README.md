# COVID-19 API

![covid19_api](https://user-images.githubusercontent.com/872589/83847861-46a73c80-a70d-11ea-83b4-f333505544d7.png)

Website: https://covid19inf.herokuapp.com/

API: https://covid19inf.herokuapp.com/api/

All data used from the [COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports)

Usage:

### All

```
curl https://covid19inf.herokuapp.com/api/

{
"06-04-2020":[{"Country_Region":"US","Confirmed":1872660,"Deaths":108211,"Recovered":485002,"Active":1334501,"Last_Update":"2020-06-05
02:33:06","Latitude":"34.22333378","Longitude":"-82.46170658","Province_State":{"South
Carolina":{"Country_Region":"US","Confirmed":421,"Deaths":8,"Recovered":0,"Active":413,"Last_Update":"2020-06-05
02:33:06","Latitude":"34.97281497","Longitude":"-81.18085944","Combined_Key":"York,
South Carolina,
US"},"Louisiana":{"Country_Region":"US","Confirmed":178,"Deaths":2,"Recovered":0,"Active":176,"Last_Update":"2020-06-05
02:33:06","Latitude":"31.94449367","Longitude":"-92.63789413","Combined_Key":"Winn,
Louisiana,
US"},"Virginia":{"Country_Region":"US","Confirmed":77,"Deaths":3,"Recovered":0,"Active":74,"Last_Update":"2020-06-05
02:33:06","Latitude":"37.24374789","Longitude":"-76.54412815","Combined_Key":"York,
Virginia,
US"}
```

### Latest

```
curl https://covid19inf.herokuapp.com/api/latest/

{"US":{"Confirmed":1872660,"Deaths":108211,"Recovered":485002,"Active":1334501,"Last_Update":"2020-06-05
02:33:06","Latitude":"34.22333378","Longitude":"-82.46170658","Province_State":{"South
Carolina":{"Country_Region":"US","Confirmed":421,"Deaths":8,"Recovered":0,"Active":413,"Last_Update":"2020-06-05
02:33:06","Latitude":"34.97281497","Longitude":"-81.18085944","Combined_Key":"York,
South Carolina,
US"},"Louisiana":{"Country_Region":"US","Confirmed":178,"Deaths":2,"Recovered":0,"Active":176,"Last_Update":"2020-06-05
02:33:06","Latitude":"31.94449367","Longitude":"-92.63789413","Combined_Key":"Winn,
Louisiana,
US"},"Virginia":{"Country_Region":"US","Confirmed":77,"Deaths":3,"Recovered":0,"Active":74,"Last_Update":"2020-06-05
02:33:06","Latitude":"37.24374789","Longitude":"-76.54412815","Combined_Key":"York,
Virginia, US"}
```

### Top countries by case (Confirmed, Deaths, Recovered)

```
curl https://covid19inf.herokuapp.com/api/top/

{"US":1872660,"Brazil":614941,"Russia":440538,"United Kingdom":283079,
"Spain":240660,"Italy":234013,"India":226713,"France":189569,"Germany":184472,
"Peru":183198}
```

```
curl https://covid19inf.herokuapp.com/api/top/?case=Deaths

{"US":108211,"United Kingdom":39987,"Brazil":34021,"Italy":33689,"France":29068,
"Spain":27133,"Mexico":12545,"Belgium":9548,"Germany":8635,"Iran":8071}
```

### New cases (Confirmed, Deaths, Recovered)

```
curl https://covid19inf.herokuapp.com/api/new/

{"Brazil":30925,"US":21140,"India":9889,"Russia":8823,"Pakistan":4801,
"Chile":4664,"Mexico":4442,"Peru":4284,"Iran":3574,"South Africa":3267}
```

```
curl https://covid19inf.herokuapp.com/api/new/?case=deaths

{"Brazil":1473,"US":1036,"Mexico":816,"India":275,"United Kingdom":176,
"Russia":168,"Canada":138,"Peru":137,"Italy":88,"Pakistan":82,"Chile":81,
"Iran":59,"South Africa":56,"France":44,"Colombia":42,"Egypt":38,
"Bangladesh":35,"Germany":33}
```

### By date

```
curl https://covid19inf.herokuapp.com/api/?date=04-30-2020

{"US":{"Confirmed":1069424,"Deaths":62996,"Recovered":153947,"Active":878169,"Last_Update":"2020-05-01
02:32:28","Latitude":"34.22333378","Longitude":"-82.46170658","Province_State":{"South
Carolina":{"Country_Region":"US","Confirmed":210,"Deaths":3,"Recovered":0,"Active":207,"Last_Update":"2020-05-01
02:32:28","Latitude":"34.97281497","Longitude":"-81.18085944","Combined_Key":"York,
South Carolina, US"}
```

### By country name

```
curl https://covid19inf.herokuapp.com/api/?name=Serbia

{"Country":"Serbia","Confirmed":11523,"Deaths":245,"Recovered":6852,"Active":4426,"Last_Update":"2020-06-04 02:33:14"}
```

### By country name and date

```
curl https://covid19inf.herokuapp.com/api/\?name\=Serbia\&cdate\=06-02-2020

{"Country":"Serbia","Confirmed":11454,"Deaths":245,"Recovered":6766,"Active":4443,"Last_Update":"2020-06-03 02:33:13"}
```
