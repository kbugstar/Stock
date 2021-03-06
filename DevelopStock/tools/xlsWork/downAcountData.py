#coding=utf-8
import getopt
import tushare as ts
import numpy as np
import pandas as pd
import os,time,sys,re,datetime
# import csv
# import scipy
# import re
import urllib.request as urllib2
# import xlwt
from bs4 import BeautifulSoup 
# from html.parser import HTMLParser  
# from urllib import request
# from urllib import parse
# from urllib.request import urlopen
import json
import random
# fh
import lxml.html
from lxml import etree
from pandas.io.html import read_html
from pandas.compat import StringIO
import xlwt
from datetime import datetime,timedelta

class RandomHeader:
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
            "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
            "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
            "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)"
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    def GetHeader(self):
        headers={"User-Agent":random.choice(self.user_agent_list)}
        return headers
class AccountPd:
    '''
    获取财务数据 to csv
    pandas 
    '''
    def __init__(self,destPath=".\\Account\\"):
        self.code =""
        self.item =""
        self.filename =""
        self.text =""
        ts.set_token('582c8c9ab1bd9e3e14d5d60527d63affb8c310fba3fb9f5d7853bf9c')
        self.pro = ts.pro_api()
        # self.wb = xlwt.Workbook()                            #生成xls表
        # self.wsZcfzb = self.wb.add_sheet(u'资产负债表')       #填加 资产负债表 
        # self.wsLrb = self.wb.add_sheet(u'利润表')             #填加 利润表 
        # self.wsXjllb = self.wb.add_sheet(u'现金流量表')       #填加 现金流量表 
        # self.sheet =self.wsZcfzb
        self.destPath =destPath
        if os.path.exists(self.destPath):                     #检测路径是否存在,不存在则创建路径
            print("current path=%s"%(os.getcwd()))
            print("%s exist"%(self.destPath))
            pass
        else:
            os.mkdir(destPath)
            print("current path=%s"%(os.getcwd()))
            print("create %s"%(self.destPath))

    def GetFullAcount(self,Code,Name,typeQ ='year'):
        '''
        按年度或者报告季读取报表
        code：股票代码
        name: 股票名称
        typeQ: year -按年度读取 ,其他 按报告季节
        '''
        # self.sheet = self.wsZcfzb
        #资产负债表
        if typeQ=='year':
            nType ='?type=year'
        else:
            nType=''
        
        Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html%s'%(nType) #资产负债表
        zcfzb =self.GetZcfzb(Url1,Code)
       

        # self.sheet = self.wsLrb
        Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html%s'%(nType) #利润表
        lrb =self.GetZcfzb(Url1,Code)

        # self.sheet = self.wsXjllb
        Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html%s'%(nType) #现金流量表
        llb =self.GetZcfzb(Url1,Code)
        # Name =Name.replace('*', '')
        # if len(self.filename)<=0:
        #     self.wb.save(self.destPath+Name+'('+Code+').csv')
        # else:
        #     self.wb.save(self.destPath+self.filename+'_'+Name+'('+Code+').csv')
        
        # zcfzb.to_excel("%s\%s(%s_%s_zcfzb).xlsx"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期')
        # lrb.to_excel("%s\%s(%s_%s_lrb).xlsx"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期')
        # llb.to_excel("%s\%s(%s_%s_llb).xlsx"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期')
        zcfzb.to_csv("%s\%s(%s_%s_zcfzb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        lrb.to_csv("%s\%s(%s_%s_lrb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        llb.to_csv("%s\%s(%s_%s_llb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
 
    def GetZcfzb(self,url,code):
        '''
        url - 读取链接
        code -股票代码
        '''
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")
        #获取财务报表的表头
        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        j =0
        df = pd.DataFrame()
        data0 =[]
        for row in table0.findAll("tr"):
            j+=1
            cells = row.findAll("td") 
            k =len(cells)
            if k<=0:
                cells =row.findAll("th")
                
                # self.sheet.write(j, 0, cells[0].text)
                data0.append(cells[0].text)
                continue
            # self.sheet.write(j, 0, cells[0].text)  
            data0.append(cells[0].text)   
        # df =df.append(data0)   
        # print(df) 
        #获取财务报表的数据
        table = soup.find("table",{"class":"table_bg001 border_box limit_sale scr_table"})
        df1 = pd.DataFrame()
        col_row=[]
        
        j=0
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            data_row =[]
            if len(cells) > 0:#
                i = 0
                lencell = len(cells)#统计财务报表的年数            
                while i < len(cells):
                    # self.sheet.write(j, i+1, cells[i].text)
                    data_row.append(cells[i].text)                                        
                    i=i+1
                # df1 =df1.append(data1)
                if(len(data_row)>1):    
                    data1=dict(zip(col_row,data_row))
                    pds =pd.Series(data1,name =data0[j-1])
                    df1 =df1.append(pds)   
            else:
                cells = row.findAll("th")
                i=0
                while i<len(cells):
                    # self.sheet.write(j,i+1,cells[i].text)
                    col_row.append(cells[i].text)  
                    i=i+1

        zcfzb = df1.T
        # zcfzb.set_index('报告日期', inplace=True)
        zcfzb=zcfzb.sort_index()
        cols =zcfzb.columns.values.tolist()
        for col in cols:
            zcfzb[col] = zcfzb[col].str.replace(',','')
            zcfzb[col] = zcfzb[col].str.replace('--','0')
        zcfzb =zcfzb.apply(lambda col:pd.to_numeric(col, errors='coerce'))
        zcfzb.fillna(0,inplace=True)
        return zcfzb

    def Get10jqkaAccount(self,Code,Name,typeQ ='year'):
        '''
        同花顺获取数据
        http://basic.10jqka.com.cn/api/stock/finance/' + $("#stockCode").val() + '_' + reportType + '.json',
        '''
        url_10jqka_base ="http://basic.10jqka.com.cn/api/stock/finance/"
        df_all =pd.DataFrame()
        #资产负债表
        url_zcfzb =url_10jqka_base+"%s_debt.json"%Code
        zcfzb =self.Get10jqkaAccountBase(url_zcfzb,typeQ)
        df_all =df_all.append(zcfzb)
        #利润表
        url_lrb =url_10jqka_base+"%s_benefit.json"%Code
        lrb =self.Get10jqkaAccountBase(url_lrb,typeQ)
        df_all =df_all.append(lrb)
        #现金流量表
        url_llb =url_10jqka_base+"%s_cash.json"%Code
        llb =self.Get10jqkaAccountBase(url_llb,typeQ)
        df_all =df_all.append(llb)
        # 
        # zcfzb.to_csv("%s\%s(%s_%s_zcfzb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        # lrb.to_csv("%s\%s(%s_%s_lrb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        # llb.to_csv("%s\%s(%s_%s_llb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        # df_all.to_csv("%s\%s(%s_%s_all).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        df_all.to_csv("%s\%s(%s_all).csv"%(self.destPath,Code,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
    def Get10jqkaAccountBase(self,url,type='year'):
        '''
        同花顺获取数据
        http://basic.10jqka.com.cn/api/stock/finance/000002_debt.json #资产负债表
        http://basic.10jqka.com.cn/api/stock/finance/000002_benefit.json #利润表
        http://basic.10jqka.com.cn/api/stock/finance/000002_cash.json #现金流量表
        http://basic.10jqka.com.cn/api/stock/finance/000002_each.json # 主要指标 每股能力
        http://basic.10jqka.com.cn/api/stock/finance/000002_grow.json # 主要指标 成长能力
        http://basic.10jqka.com.cn/api/stock/finance/000002_pay.json  # 主要指标 偿债能力
        http://basic.10jqka.com.cn/api/stock/finance/000002_operate.json # 主要指标 运营能力

        '''
        # headers={
        # # 'Referer': 'http://basic.10jqka.com.cn/000002/finance.html',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'        
        # }
        getH =RandomHeader()
        headers =getH.GetHeader()
        # print(headers)
        req = urllib2.Request(url, headers = headers)
        content = urllib2.urlopen(req).read()
        text =content.decode('utf8')
        jsonobj = json.loads(text)
        data =jsonobj['flashData']
        dataList =json.loads(data)
        title =dataList['title']
        for k in range(1,len(title),1):
            title[k]="%s(%s)"%(title[k][0] ,title[k][1])
        resultData =[]
        if(type=='year'):
            year  =dataList['year']#年报
            resultData =year
        else:
            report =dataList['report']#季报
            resultData =report
        # for k in range(len(resultData)):
        #     for j in range(len(resultData[k])):
        #         ret_str =str(resultData[k][j])
        #         if(ret_str.find('亿')>=0):
        #             continue
        #         else:
        #             pos =ret_str.find('万')
        #             if(pos>=0):
        #                 part = ret_str[0:pos]
        #                 if(self.is_number(part)):
        #                     resultData[k][j]=str(float(part)/10000)+'亿'

        df =pd.DataFrame(data=resultData,index=title)
        # print(df.T)
        return df
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass
    
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
    
        return False
    def GetCodeList(self):
        try:
            print("------开始读取股票基本信息.....")
            ddf =ts.get_stock_basics()
            ddf =ddf.sort_index()

            ddf.to_csv('%s\StockClass.csv'%(self.destPath),encoding='utf_8_sig')
            print("------结束读取股票基本信息.....")
        except Exception as ex:
            print("------读取股票失败.....")
            pass

    def GetFhpgSina(self,code,name):
        '''
        get fen hong and pei gu
        http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/600519.phtml
        '''
        pd.options.mode.chained_assignment = None
        dataArr =pd.DataFrame()
        try:
            Id ="sharebonus_1"
            Id2="sharebonus_2"
            FINIANCE_SINA_URL ='http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/%s.phtml'
            furl = FINIANCE_SINA_URL%(code)        #获取数据，标准处理方法
            getH =RandomHeader()
            headers =getH.GetHeader()
            request = urllib2.Request(furl, headers = headers)
            text = urllib2.urlopen(request, timeout=5).read()
            # text = text.decode('gbk')
            # html = lxml.html.parse(StringIO(text))        #分离目标数据
            # # res = html.xpath("//table[@id=\"BalanceSheetNewTable0\"]")#ProfitStatementNewTable0

            # res = html.xpath(("//table[@id=\"%s\"]")%Id)
            # sarr = [etree.tostring(node).decode('gbk') for node in res]        #存储文件
            # sarr = ''.join(sarr)
            # sarr = '<table>%s</table>'%sarr        #向前滚动一年
       
            # df = read_html(sarr)[0]

            # dataArr = [dataArr, df]
            # # dataArr = pd.concat(dataArr, axis=1, join='inner')
            # dataArr = pd.concat(dataArr, axis=1)
            # columns =[]
            # cnt =len(dataArr.columns.levels[2])
            # for k in range(cnt):
            #     columns.append(dataArr.columns.levels[2][dataArr.columns.codes[2][k]])
            # dataArr.columns =columns
            dataArr =self.GetFhpgBase(text,Id)
            # dataArr = pd.concat(dataArr, axis=1)
            columns =[]
            cnt =len(dataArr.columns.levels[2])
            fhfan =dataArr.columns.levels[1][1]
            pos =fhfan.find('每')
            fhgs =fhfan[pos+1:-2]

            for k in range(cnt):
                columns.append(dataArr.columns.levels[2][dataArr.columns.codes[2][k]])
            dataArr.columns =columns
            dataArr =dataArr.drop(['查看详细'],axis=1)
            dataArr['方案'] =fhgs
            # 配股
            columns =[]
            dataArr2 =self.GetFhpgBase(text,Id2)
            cnt =len(dataArr2.columns.levels[1])
            for k in range(cnt):
                columns.append(dataArr2.columns.levels[1][dataArr2.columns.codes[1][k]])
            dataArr2.columns =columns
            pggs =columns[1][columns[1].find('每')+1 : columns[1].find('股配')]
            dataArr2 =dataArr2.drop(['查看详细'],axis=1)
            dataArr2['方案'] =pggs
            dataArr2['实际配股数'] =0.0
            pg_len =len(dataArr2)
            pg_sjpgs ='0.0'
            for ind in range(pg_len):
                pg_sjpgs ='0.0'
                date_ggrq =dataArr2['公告日期'][ind]
                df_pgxx =self.GetPgXX(code,'2',date_ggrq)
                len_pgxx =len(df_pgxx)
                for k in range(len_pgxx):
                    if(df_pgxx[0][k]=='实际配股数'):
                        if(df_pgxx[1][k]=='--'):
                            pg_sjpgs ='0.0'
                        else:
                            pg_sjpgs =df_pgxx[1][k]
                        break
                
                dataArr2['实际配股数'][ind] =pg_sjpgs

            # outFile ="%s\%s(%s_fhpg).xls"%(self.destPath,code,name)
            # write = pd.ExcelWriter(outFile)

            # if(len(dataArr)>=0):
            #     # columns =['公告日期','分红年度','送股','转增','派息','股权登记日','除权除息日','红股上市日']
            #     # '公告日期'	'送股(股)'	'转增(股)'	'派息(税前)(元)'	'进度'	'除权除息日'	'股权登记日'	'红股上市日'
            #     # 序号	股票代号	公告年度	公告日期	分红年度	送股	转增	派息	股权登记日	除权除息日	红股上市日

            #     # dataArr =dataArr[columns]
            #     dataArr.to_excel(write,sheet_name='历史分红',index=False)
            #     write.save() 
            # else:
            #     print("          %s(%s) 分红数据不存在"%(code,name))
     
        except Exception as ex:
             print("           %s(%s) 分红数据读取异常[%s]"%(code,name,ex))

        return dataArr,dataArr2#分红 配股

    def GetFhpgBase(self,text,Id):
        '''
        分红 和 配股 的公共 部分 代码
        '''
        text = text.decode('gbk')
        html = lxml.html.parse(StringIO(text))        #分离目标数据
        # res = html.xpath("//table[@id=\"BalanceSheetNewTable0\"]")#ProfitStatementNewTable0

        res = html.xpath(("//table[@id=\"%s\"]")%Id)
        sarr = [etree.tostring(node).decode('gbk') for node in res]        #存储文件
        sarr = ''.join(sarr)
        sarr = '<table>%s</table>'%sarr        #向前滚动一年
    
        df = read_html(sarr)[0]
        #all_href =soup.find_all('a', href=True)
        return df#,all_href

    def GetPgXX(self,code,typeL,end):
        '''
        get detail message 
        get 实际配股数
        http://money.finance.sina.com.cn/corp/view/vISSUE_ShareBonusDetail.php?stockid=000001&type=2&end_date=2000-10-23
        '''
        try:
            Id ="sharebonusdetail"
            FINIANCE_SINA_URL ='http://money.finance.sina.com.cn/corp/view/vISSUE_ShareBonusDetail.php?stockid=%s&type=%s&end_date=%s'
            furl = FINIANCE_SINA_URL%(code,typeL,end)        #获取数据，标准处理方法
            getH =RandomHeader()
            headers =getH.GetHeader()
            request = urllib2.Request(furl, headers = headers)
            text = urllib2.urlopen(request, timeout=5).read()
            text = text.decode('gbk')
            html = lxml.html.parse(StringIO(text))        #分离目标数据

            res = html.xpath(("//table[@id=\"%s\"]")%Id)
            sarr = [etree.tostring(node).decode('gbk') for node in res]        #存储文件
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr        #向前滚动一年
            df = read_html(sarr)[0]
            return df            
        except:
            return pd.DataFrame()

    def GetZfSina(self,code):
        '''
        增发
        http://money.finance.sina.com.cn/corp/go.php/vISSUE_AddStock/stockid/000001.phtml
        '''

        url ="http://money.finance.sina.com.cn/corp/go.php/vISSUE_AddStock/stockid/%s.phtml"%(code)
        # headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        getH =RandomHeader()
        headers =getH.GetHeader()
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return pd.DataFrame()
        html_encode='gb2312'
        soup = BeautifulSoup(content.decode(html_encode,errors='ignore'), "html.parser")#html_encode='gb2312'
        # soup = BeautifulSoup(content,features="lxml")
        #获取财务报表的表头
        # div tagmain
        div0 = soup.find("div",{"class":"tagmain"})
        table2 = div0.find("table",{"class":"table2"})
        if(table2 is None):
            return pd.DataFrame()
        a =table2.findAll("a")
        a_len =len(a)
        # for k in range(a_len -1):
        #     print(a[k])
        table = div0.findAll("table")
        table_len =len(table)
        df1 = pd.DataFrame()
        col_row =[]
        for k in range(1,table_len-1,1):
            data_row =[]
            th_text =table[k].find("th").text
            tr_all =table[k].findAll("tr")
            tr_all_len =len(tr_all)
            pos =th_text.find("：")
            if k==1:
                col_row.append(th_text[pos-4:pos])
            data_row.append(th_text[pos+1:])
            for d in range(1,tr_all_len):
                td_all =tr_all[d].findAll("td")
                if(k==1):
                    col_row.append(td_all[0].text)
                
                data_row.append(td_all[1].text)

            data1=dict(zip(col_row,data_row))
            pds =pd.Series(data1,name ="")
            df1 =df1.append(pds)  
        df_len =len(df1)
        for k in range(df_len):
            df1['发行价格：'].values[k] =float(df1['发行价格：'].values[k].replace('元',''))
            if(df1['实际发行数量：'].values[k].find('万股')>=0):
                df1['实际发行数量：'].values[k] =df1['实际发行数量：'].values[k].replace('万股','')
                df1['实际发行数量：'].values[k] =float(df1['实际发行数量：'].values[k])*10000
            else:
                df1['实际发行数量：'].values[k] =float(df1['实际发行数量：'].values[k].replace('股',''))
        df1['增发'] =df1['发行价格：']*df1['实际发行数量：']/100000000
        return df1
    def GetGJ(self,code,start,end):
        '''
        股价 tushare
        '''
        start =start.replace('-','')
        end   =end.replace('-','')
        if(code.find('.S')<0):
            if(code >'600000'):
                code =code+'.SH'
            else:
                code =code +'.SZ'

        df1 = self.pro.daily(ts_code=code, start_date=start, end_date=end)
        return df1
    def GetSS_Sina(self,code):
        '''
        诉讼仲裁
        诉讼提取：所有日期及相应案件名称
        http://money.finance.sina.com.cn/corp/go.php/vGP_Lawsuit/stockid/000001.phtml
        '''
        url ="http://money.finance.sina.com.cn/corp/go.php/vGP_Lawsuit/stockid/%s.phtml"%(code)
        getH =RandomHeader()
        headers =getH.GetHeader()
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return pd.DataFrame()
        html_encode='gb2312'
        soup = BeautifulSoup(content.decode(html_encode,errors='ignore'), "html.parser")#html_encode='gb2312'
        # soup = BeautifulSoup(content,features="lxml")
        table = soup.find("table",{"id":"lawsuit"})
        # tbody_All =table.findAll("tbody")
        # tbody_all_len =len(tbody_All)
        # col_row =[]
        # df1 =pd.DataFrame()
        # for k in range(tbody_all_len):
        #     tr_all =tbody_All[k].findAll("tr")
        #     tr_all_len =len(tr_all)
        #     data_row =[]
        #     for j in range(tr_all_len):
        #         td_all = tr_all[j].findAll("td")
        #         if(k==0):
        #             col_row.append(td_all[0].text)
        #         data_row.append(td_all[1].text)
        #     data1=dict(zip(col_row,data_row))
        #     pds =pd.Series(data1,name ="")
        #     df1 =df1.append(pds)  
        if(table is None):
            return pd.DataFrame(columns=['公告日期','案件名称'])
        tbody = table.find("tbody")
        tr_all =tbody.findAll("tr")
        df1 =pd.DataFrame()
        k =0
        row_cnt =0
        col_row =[]
        tr_all_len =len(tr_all)
        while(1):
            if(k>=tr_all_len):
                break
            td_all =tr_all[k].findAll("td")
            if(len(td_all)==0):
                data_row =[]
                th =tr_all[k].findAll("th")
                if(len(th)>0):
                    if row_cnt ==0:
                        pos =th[0].text.find(':')
                        col_row.append(th[0].text[pos-4:pos])
                    data_row.append(th[0].text[pos+1:])  
                k =k+1
                if(k>=tr_all_len):
                    break
                while(1):
                    td_all =tr_all[k].findAll("td") 
                    if(len(td_all)==0):
                        break
                    else:
                        if(len(td_all)==2):
                            if(row_cnt==0):
                                col_row.append(td_all[0].text)
                            data_row.append(td_all[1].text)  
                    k =k+1
                    if(k>=tr_all_len):
                        break
            data1=dict(zip(col_row,data_row))
            pds =pd.Series(data1,name ="")
            df1 =df1.append(pds)                  
            row_cnt =row_cnt+1 

        return df1            
    def GetWGJL_Sina(self,code):
        '''
        违规记录
        违规提取：所有日期及相应处分类型
        http://money.finance.sina.com.cn/corp/go.php/vGP_GetOutOfLine/stockid/000001.phtml
        '''
        url ="http://money.finance.sina.com.cn/corp/go.php/vGP_GetOutOfLine/stockid/%s.phtml"%(code)
        getH =RandomHeader()
        headers =getH.GetHeader()
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return pd.DataFrame()
        html_encode='gb2312'
        soup = BeautifulSoup(content.decode(html_encode,errors='ignore'), "html.parser")#html_encode='gb2312'
        # soup = BeautifulSoup(content,features="html.parser")
 
        table =soup.find("table",{"id":"collectFund_1"})
        if(table is None):
            return pd.DataFrame(columns=['公告日期','处分类型'])
        tbody = table.find("tbody")
        tr_all =tbody.findAll("tr")
        df1 =pd.DataFrame()
        k =0
        row_cnt =0
        col_row =[]
        tr_all_len =len(tr_all)
        while(1):
            if(k>=tr_all_len):
                break
            td_all =tr_all[k].findAll("td")
            if(len(td_all)==0):
                data_row =[]
                th =tr_all[k].findAll("th")
                if(len(th)>0):
                    if row_cnt ==0:
                        pos =th[0].text.find(':')
                        col_row.append(th[0].text[pos-4:pos])
                    data_row.append(th[0].text[pos+1:])  
                k =k+1
                if(k>=tr_all_len):
                    break
                while(1):
                    td_all =tr_all[k].findAll("td") 
                    if(len(td_all)==0):
                        break
                    else:
                        if(len(td_all)==2):
                            if(row_cnt==0):
                                col_row.append(td_all[0].text)
                            data_row.append(td_all[1].text)  
                    k =k+1
                    if(k>=tr_all_len):
                        break
            data1=dict(zip(col_row,data_row))
            pds =pd.Series(data1,name ="")
            df1 =df1.append(pds)                  
            row_cnt =row_cnt+1   


        # tbody_all =table.findAll("tbody")

        # thread_all =table.findAll("thead")
        # thread_all_len =len(thread_all)
        # col_row =[]
        # df1 =pd.DataFrame()
        # for k in range(thread_all_len):
        #     th =thread_all.find("th")
        #     tr_all =tbody_all[k+1].findAll("tr")
        #     td_all =tr_all[2].findAll("td")
        #     pos =th.text.find(':') 
        #     data_row =[]           
        #     if(k==0):
        #         col_row.append(th.text[pos-4:pos])
        #         col_row.append(td_all[0].text)
        #     data_row.append(td_all[1].text)
        #     data_row.append(th.text[pos+1:])            
        # data1=dict(zip(col_row,data_row))
        # pds =pd.Series(data1,name ="")
        # df1 =df1.append(pds)      
        return df1

    def Get_fhpg_SS_Wgjl_Zf(self,code):
        '''
        数据源 sina tushare
            分红配股 增发 股价
            诉讼 违规记录
        '''
        pd.options.mode.chained_assignment = None

        fh,pg =self.GetFhpgSina(code,"")
        #
        try:
            fh_date =fh['除权除息日']
            fh['除权除息日股价'] =0.0
            fh['派息调整'] =0.0
            fh['转增(股)'] =fh['转增(股)'].astype('float64')
            fh['派息(税前)(元)'] =fh['派息(税前)(元)'].astype('float64')
            fh['送股(股)'] =fh['送股(股)'].astype('float64')
            for k in range(len(fh_date)):
                start =fh_date[k]
                end   =fh_date[k]
                if(start.find('暂时没有数据')>=0):
                    continue
                if(start =='--'):
                    continue
                gj =self.GetGJ(code,start,end)
                # print('start =%s end =%s'%(start,end))
                # print(gj)
                
                fh['派息(税前)(元)'][k] =float(fh['派息(税前)(元)'][k])/(float(fh['方案'][k]))
                fh['送股(股)'][k] =float(fh['送股(股)'][k])/(float(fh['方案'][k]))
                fh['转增(股)'][k] =float(fh['转增(股)'][k])/(float(fh['方案'][k]))
                if(len(gj)>0):
                    # fh['除权除息日股价'][k] =gj['close'][0]
                    fh['除权除息日股价'][k] =gj['open'][0]
                    fh['派息调整'][k] =fh['派息(税前)(元)'][k]/(fh['除权除息日股价'][k])
            # save fh
            if(len(fh)>0):
                fh= fh[fh['除权除息日']!='--']
                fh_group =fh
                fh_group['year'] =fh['公告日期'].str[:4]
                fh_group1 =fh_group.groupby('year').sum()
                fh_group2 =fh_group1.sort_values(by=['year'], ascending=False)
                fh_group2.to_csv("%s\%s_fh.csv"%(self.destPath,code),index_label=u'',encoding='utf_8_sig')
        except:
            pass
        try:
            pg_date =pg['除权日']
            pg['除权日前日股价'] =0.0

            pg['配股调整'] =0.0
            pg['配股募资金额(亿)'] =0.0
            pg['每股配股数'] =0.0
            pg['除权价'] =0.0
            
            for k in range(len(pg_date)):

                start =pg_date[k]

                if(start.find('暂时没有数据')>=0):
                    continue
                if(start =='--'):
                    continue
                start_date =datetime.strptime(start, '%Y-%m-%d')
                end_date =start_date + timedelta(days = -10)
                end =end_date.strftime('%Y-%m-%d')
                
                gj =self.GetGJ(code,end,start)
                if(len(gj)>1):
                    pg['除权日前日股价'][k] =gj['close'][1]
                    '''
                    配股调整 =（1 – 配股价/除权价）*每股配股数
                    除权价= （除 权前一日收盘价 + 配股价*每股配股数）/ （1 + 每股配股数）
                    '''
                    pg['每股配股数'][k] =pg['配股方案(每10股配股股数)'][k]*1.0/10.0
                    pg['除权价'][k] =(pg['除权日前日股价'][k] + pg['配股价格(元)'][k]*pg['每股配股数'][k])/(1 + pg['每股配股数'][k])
                    pg['配股调整'][k] =  (1- pg['配股价格(元)'][k]/pg['除权价'][k])*pg['每股配股数'][k]
                    pg['配股募资金额(亿)'][k] = float(pg['实际配股数'][k])*float(pg['配股价格(元)'][k])/100000000.0
            # save pg 
            if(len(pg)>0):  
                pg= pg[pg['除权日']!='--']            
                pg_group =pg
                pg_group['year'] =pg['公告日期'].str[:4]
                pg_group1 =pg_group.groupby('year').sum()
                pg_group2 =pg_group1.sort_values(by=['year'], ascending=False)
                pg_group2.to_csv("%s\%s_pg.csv"%(self.destPath,code),index_label=u'',encoding='utf_8_sig')  
        except:
            pass
        zf =self.GetZfSina(code)
        try:
            if len(zf)>0:
                zf_group =zf
                zf_group['year'] =zf['公告日期'].str[:4]
                zf_group1 =zf_group.groupby('year').sum()
                zf_group2 =zf_group1.sort_values(by=['year'], ascending=False)        
                zf_group2.to_csv("%s\%s_zf.csv"%(self.destPath,code),index_label=u'',encoding='utf_8_sig') 
        except:
            pass
        # save zf
        ss =self.GetSS_Sina(code)
        try:
            if(len(ss)>0):
                ss =ss[['公告日期','案件名称']]
                ss.to_csv("%s\%s_ss.csv"%(self.destPath,code),index_label=u'',encoding='utf_8_sig') 
        except:
            pass
        # save ss
        wgjl =self.GetWGJL_Sina(code)
        try:
            if(len(wgjl)>0):
                wgjl =wgjl[['公告日期','处分类型']]
                wgjl.to_csv("%s\%s_wgjl.csv"%(self.destPath,code),index_label=u'',encoding='utf_8_sig') 
        except:
            pass
        # save wgjl


def main():
    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2]) 
    
    destPath ="%s\\Account"%(sys.argv[1]) 
    xlsTest =AccountPd(destPath=destPath)
    code =sys.argv[2]

    if(code=='stock'):
        xlsTest.GetCodeList()
    else:
        # print(sys.argv[3]) 
        name =sys.argv[3]
        if(name =='fh'):
            xlsTest.Get_fhpg_SS_Wgjl_Zf(code)
        else:
            name =""
            # xlsTest.GetFullAcount(code,name,typeQ='year')
            # xlsTest.GetFullAcount(code,name,typeQ='quarter')
            xlsTest.Get10jqkaAccount(code,name,typeQ='year')
            xlsTest.Get10jqkaAccount(code,name,typeQ='quarter')
if __name__ == '__main__':
    main()
    # xlsTest =AccountPd()
    # xlsTest.GetZfSina('000001')
    # xlsTest.GetFhpgSina("000001","test")
    # xlsTest.Get10jqkaAccount('000651','test',typeQ='year')
    # xlsTest.Get10jqkaAccount('000651','test',typeQ='quarter')
    # xlsTest.Get_fhpg_SS_Wgjl_Zf('600968')
    # xlsTest.Get_fhpg_SS_Wgjl_Zf('601857')
    # xlsTest.Get_fhpg_SS_Wgjl_Zf('000409')
    # xlsTest.Get_fhpg_SS_Wgjl_Zf('000598')
    
    # xlsTest.Get_fhpg_SS_Wgjl_Zf('002260')
    # xlsTest.Get_fhpg_SS_Wgjl_Zf('600089')
    # xlsTest.Get_fhpg_SS_Wgjl_Zf('000001')
    # xlsTest.GetFhpgSina('000001','')
