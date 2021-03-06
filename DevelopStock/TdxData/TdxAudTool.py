import os
from PyQt5 import QtCore, QtGui, QtWidgets
from TdxAudToolBase import Ui_Dialog
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import datetime
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from  Qt5WithMatplot import *
from datetime import datetime, date, timedelta
import threading
from PyQt5.QtWidgets import QMessageBox
from processTdxDay import *

from multiprocessing import Process,Queue

str_msgQ = Queue()
class TdxAudTool_Dialog(Ui_Dialog):#QtWidgets.QWidget
    signal = pyqtSignal(str,int)
    def __init__(self):
        super(TdxAudTool_Dialog,self).__init__()
        super().setupUi(Dialog)
    def setupUi(self,Dialog):

        Dialog.setObjectName("dlg")

        #实例化列表模型，添加数据
        self.qsL=QStringListModel()
        self.Test=[]
        self.processInt =0#进度条位置
        self.setProcessBarPos(0)#设置进度条位置
        self.MAX_THREAD_NUM =5#最多并发数
        self.d0 =None#绘图上的数据存储
        self.d1 =None#绘图下的数据存储
        #设置模型列表视图，加载数据列表
        self.qsL.setStringList(self.Test)
        #设置列表视图的模型
        self.lv_msg.setModel(self.qsL)    
        self.signal.connect(self.callbacklog)
        self.th2 =None#线程的实例
        self.threadList =[]#进程的list
        #设置数据层次结构，4行4列
        self.model=QStandardItemModel()#龙虎榜的tableview的数据
        self.hy_model=QStandardItemModel()#行业分析的tableview的数据

        self.btn_lhb.clicked.connect(self.on_btn_lhb_click)#获取龙虎榜
        self.btn_tdx_path.clicked.connect(self.on_btn_tdx_path_click)#选取通达信的路径
        self.btn_read_stock.clicked.connect(self.on_btn_read_stock_click)#从通达信路径读取数据
        self.btn_clearMsg.clicked.connect(self.on_btn_clearMsg_click)#清理列表的数据
        self.btn_getValue.clicked.connect(self.on_btn_getValue_click)#从数据库读取数据
        self.btn_drawPic.clicked.connect(self.on_btn_drawPic_click)#绘制选择的图像
        self.btn_tqHyfx.clicked.connect(self.on_btn_tqHyfx_click)#提取行业数据
        self.btn_stop_readTdx.clicked.connect(self.on_btn_stop_readTdx_click)
        # self.btn_stop_readTdx.hide()
        self.tbl_hyfx.setSortingEnabled(True)#设置table排序
        self.tv_lhb.setSortingEnabled(True)#设置table排序
        # 
        now_time = datetime.datetime.now()#现在
        end = now_time.strftime("%Y-%m-%d")
        yesterday =now_time +timedelta(days = -1) #昨天
        start =yesterday.strftime('%Y-%m-%d')
        self.dateEdit_Start.setDate(QDate.fromString(start, 'yyyy-MM-dd'))#start time
        self.dateEdit_End.setDate(QDate.fromString(end, 'yyyy-MM-dd'))#end time
        # 
        self.comboBox.addItem('日')
        self.comboBox.addItem('周')
        self.comboBox.addItem('月')
        self.comboBox.currentIndexChanged.connect(self.comb_selectionchange)
        # 
        #启动定时器
        self.timer=QTimer()
        self.timer.timeout.connect(self.currTime)
        self.timer.start(2000)#2秒

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject) 
        #定义MyFigure类的实例
        self.Myfig = MyFigure(width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.Myfig, self)

        #在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.gridlayout = QGridLayout(self.groupBox_pic)  # 继承容器groupBox
        self.gridlayout.addWidget(self.Myfig,0,1)
        self.gridlayout.addWidget(self.toolbar,1,1)
    def on_btn_stop_readTdx_click(self):
        '''
        停止线程
        '''
        if(self.th2 is None):
            self.addListViewMessage("线程不存在")    
        else:
            if(self.th2.is_alive()==False):
                self.th2.terminal()
                self.addListViewMessage("线程停止运行,退出程序终止后台还有进程运行")  
            else:
                self.addListViewMessage("线程停止运行,退出程序终止后台还有进程运行")

                      
    def on_btn_tqHyfx_click(self):
        '''
        读取股票行业排名
        '''
        self.le_hyfxStatus.setText('正在读取')
        hyfx_code =self.le_hyfxCode.text()

        if(len(hyfx_code)==6):#检测股票代码长度
            
            hyfx =hybg()
            item,list_hyfx =hyfx.getHydbFrom163(hyfx_code)
            write = pd.ExcelWriter(hyfx.basePath+'/'+hyfx_code+'_hyfx.xls')
            df_hyfx =""
            i=0
            while i<len(list_hyfx):
                (list_hyfx[i]).to_excel(write,sheet_name=item[i],index=True)
                i =i+1
            df_hyfx =list_hyfx[2]
            write.save() 
        else:
            self.le_hyfxStatus.setText('股票代码必须6位')
            return

        if (df_hyfx is None):
            self.le_hyfxStatus.setText('数据不存在')
            return 
        if(len(df_hyfx)<=0):
            self.le_hyfxStatus.setText('数据不存在')
            return
        self.hy_model.setHorizontalHeaderLabels(['排名','名称','每股收益','销售净利率%','净资产收益率%','资产负债率%','流动比率%'])

        row =0
        for i in range(0, len(df_hyfx)):

            rowContent =df_hyfx.iloc[i]
            item=QStandardItem(rowContent['排名'])
            self.hy_model.setItem(row,0,item)
            item=QStandardItem(rowContent['名称'])
            self.hy_model.setItem(row,1,item)
            item=QStandardItem(str(rowContent['每股收益']))
            self.hy_model.setItem(row,2,item)
            item=QStandardItem(str(rowContent['销售净利率%']))
            self.hy_model.setItem(row,3,item)
            item=QStandardItem(str(rowContent['净资产收益率%']))
            self.hy_model.setItem(row,4,item)
            item=QStandardItem(str(rowContent['资产负债率%']))
            self.hy_model.setItem(row,5,item)
            item=QStandardItem(str(rowContent['流动比率%']))
            self.hy_model.setItem(row,6,item)

            row =row +1
        self.tbl_hyfx.setModel(self.hy_model) 
        self.le_hyfxStatus.setText('')

    def comb_selectionchange(self):
        '''
        comb控件
        '''
        print(self.comboBox.currentText())

    def on_btn_drawPic_click(self):
        '''
        绘制图片
        上图显示上面的股票图像
        下图显示下面的股票图像
        '''
        self.le_drawPic.setText("正在绘图")
        codeU =self.lineEdit_CodeUp.text()
        codeD =self.lineEdit_CodeDn.text()
        self.Myfig.setCodeY(codeU,codeD)
        if(self.d0 is None or self.d1 is None):
            self.le_drawPic.setText("数据不存在")
            return
        self.Myfig.drawAll(self.getSelect(),self.d0,self.d1)#绘图
        self.le_drawPic.setText("")
    def on_btn_getValue_click(self):
        '''
        重数据库提取数据
        '''
        startDay =self.dateEdit_Start.dateTime()
        startTime =startDay.toString('yyyy-MM-dd')
        endDay = self.dateEdit_End.dateTime()
        endTime =endDay.toString('yyyy-MM-dd')
        curSel =self.comboBox.currentText()
        codeU =self.lineEdit_CodeUp.text()
        codeD =self.lineEdit_CodeDn.text()
        td =TdxData()
        self.le_dbStatus.setText("")
        if(td.getDbStatus()==False):
            self.le_dbStatus.setText("数据库连接失败")
            return 
        if(curSel =="日"):
            tb_name='day_k'
        if(curSel =="周"):
            tb_name='week_k'
        if(curSel =="月"):
            tb_name='month_k'
        if(len(codeU)>0):
            sql ="select * from %s where code ='%s' and date between '%s' and '%s'  order by date asc"%(tb_name,codeU,startTime,endTime)
            data0 =td.mydb.read_sql_query(sql)
            data0.rename(columns={'date':'t'}, inplace = True)
            self.d0 =self.Myfig.prepare_data(data0)#对原始数据整理
        if(len(codeD)>0):
            sql ="select * from %s where code ='%s' and date between '%s' and '%s'  order by date asc"%(tb_name,codeD,startTime,endTime)
            data1 =td.mydb.read_sql_query(sql)
            data1.rename(columns={'date':'t'}, inplace = True)
            self.d1 =self.Myfig.prepare_data(data1)#对原始数据整理
        
        
        
        

    def getSelect(self):
        '''
        检测绘制图像的类型 加入链表中
        '''
        cb =[]
        cbv =[]
        kLine =self.cb_kLine.isChecked()
        cbv.append(kLine)
        cb.append('kLine')

        volume =self.cb_volume.isChecked()
        cbv.append(volume)
        cb.append('volume')

        macd =self.cb_MACD.isChecked()
        cbv.append(macd)
        cb.append('MACD')

        BOLL =self.cb_BOLL.isChecked()
        cbv.append(BOLL)
        cb.append('BOLL')
        
        nhd_20_31_60 =self.cb_nhd_20_31_60.isChecked()
        cbv.append(nhd_20_31_60)
        cb.append('Glue20_31_60')

        nhd31_60_120 =self.cb_nhd31_60_120.isChecked()
        cbv.append(nhd31_60_120)
        cb.append('Glue31_60_120')

        MA5 =self.cb_MA5.isChecked()
        cbv.append(MA5)
        cb.append('MA_5')

        MA10 =self.cb_MA10.isChecked()
        cbv.append(MA10)
        cb.append('MA_10')

        MA20 =self.cb_MA20.isChecked()
        cbv.append(MA20)
        cb.append('MA_20')

        MA31 =self.cb_MA31.isChecked()
        cbv.append(MA31)
        cb.append('MA_31')

        MA60 =self.cb_MA60.isChecked()
        cbv.append(MA60)
        cb.append('MA_60')

        MA120 =self.cb_MA120.isChecked()
        cbv.append(MA120)
        cb.append('MA_120')

        slopeMA5 =self.cb_slopeMA5.isChecked()
        cbv.append(slopeMA5)
        cb.append('Slope_M5')

        slopeMA10 =self.cb_slopeMA10.isChecked()
        cbv.append(slopeMA10)
        cb.append('Slope_M10')

        slopeMA20 =self.cb_slopeMA20.isChecked()
        cbv.append(slopeMA20)
        cb.append('Slope_M20')

        slopeMA31 =self.cb_slopeMA31.isChecked()
        cbv.append(slopeMA31)
        cb.append('Slope_M31')

        slopeMA60 =self.cb_slopeMA60.isChecked()
        cbv.append(slopeMA60)
        cb.append('Slope_M60')

        slopeMA120 =self.cb_slopeMA120.isChecked()
        cbv.append(slopeMA120)
        cb.append('Slope_M120')

        select =dict(zip(cb,cbv))
        return select
        ###
    def accept(self):
        print("accept")
        self.close()
    def reject(self):
        print("reject")
        self.close()

    def currTime(self):
        '''
        定时器响应函数
        '''
        self.setProcessBarPos(self.processInt)     
        if(str_msgQ.qsize()>0):
            str_msg =str_msgQ.get()
            self.addListViewMessage(str_msg)#向信息框加信息

    def closeEvent(self,event):
        '''
        退出提示
        '''
        reply =QMessageBox.question(self,"提示","后台还有进程运行，你确认退出么？",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if reply==QMessageBox.Yes:
            Dialog.accept()
        else:
            Dialog.ignore()

    def on_btn_clearMsg_click(self):
        '''
        清除信息框数据
        '''
        self.Test.clear()
        self.qsL.setStringList(self.Test)


    def on_btn_tdx_path_click(self):
        '''
        判断线程是否在运行，如果运行不进行路径设置
        '''
        self.savePath = QtWidgets.QFileDialog.getExistingDirectory(self,  
                            "浏览",  
                            "./")
        if(len(self.savePath)>0):
            self.le_tdx_path.setText(self.savePath+'/')  
            self.le_read_path.setText(self.savePath+'/vipdoc/sz/lday')#默认深证,上证路径'/vipdoc/sh/lday'


    def on_btn_read_stock_click(self):
        '''
        读取通达信/vipdoc/sz/lday目录下的日线数据
        启动线程
        '''
        if(self.th2 is None):
            self.addListViewMessage("线程启动")
            self.th2 = threading.Thread(target=self.processData, args=(), name='funciton')#线程
            self.th2.setDaemon(True)#设为守护进程
            self.th2.start()
        else:
            if(self.th2.is_alive()==False):
                self.addListViewMessage("线程启动")
                self.th2 = threading.Thread(target=self.processData, args=(), name='funciton')
                self.th2.setDaemon(True)
                self.th2.start()
            else:
                self.addListViewMessage("线程正在运行")

    def processData(self):
        '''
        线程函数
        在这个函数启动线程 分别进行读取 加快处理速度
        '''
        source =self.le_read_path.text()
        if(len(source)<=0):
            self.EmitMsgToUi("通达信路径不存在")
            return
        try:
            file_list = os.listdir(source)
        except Exception as e:
            self.EmitMsgToUi("通达信路径不正确")
            return
        td =""
        self.processInt =0
        if(self.rb_lhb.isChecked()):#读取龙虎榜
            target ="./lhb" #数据存储目录
            self.le_outpath.setText(target)
            self.ifPathExist(target)
            if self.dataLhb is None:
                self.EmitMsgToUi('')
                return
            else:
                self.EmitMsgToUi("开始读取龙虎榜上的股票数据")
                source =self.le_tdx_path.text()
                self.walkThroughtLhb(td,source,target)#遍历龙虎榜数据
                self.EmitMsgToUi("结束读取龙虎榜上的股票数据")

        
        if(self.rb_all.isChecked()):#读取通达信目录下的
            global str_msgQ
            target="./lday"
            self.le_outpath.setText(target)
            self.ifPathExist(target)
            self.EmitMsgToUi("开始通信达目录%s下的所有股票数据"%source)
            total =len(file_list)
            i =0
            for f in file_list:
                i =i+1
                self.processInt =round(1.0 * i/ total * 100,2)
                target_prefix ="tdx_"
                #启动进程
                th =Process(target=thread_day2csv_all, args=(str_msgQ,td,source,f,target,target_prefix))
                self.threadList.append(th)
                if((total -i)>=self.MAX_THREAD_NUM):
                    if(len(self.threadList)>=self.MAX_THREAD_NUM):
                        for x in self.threadList:
                            x.daemon=True
                            x.start()
                        x.join()
                        self.threadList.clear()
                else:
                    for x in self.threadList:
                        x.daemon=True
                        x.start()
                    x.join()
                    self.threadList.clear()        
            self.EmitMsgToUi("结束通信达目录%s下的所有股票数据"%source)      

    def EmitMsgToUi(self,msg):
        '''
        向界面发送信息
        '''
        self.signal.emit(msg,self.processInt)

    def walkThroughtLhb(self,td,source,target):
        '''
        读取龙虎榜的数据
        '''
        global str_msgQ
        if (self.dataLhb is None):
            return 
        total =len(self.dataLhb)
        target_prefix ='lhb_'
        for i in range(0, total):
            self.processInt =round(1.0 * i/ total * 100,2)
            code = self.dataLhb.iloc[i]['code']
            #根据股票的类型选择不同路径
            if(code >='600000'):
                tdxCode ="sh%s.day"%code
                sourceD = source +'/vipdoc/sh/lday'
            else:
                tdxCode ="sz%s.day"%code
                sourceD = source +'/vipdoc/sz/lday'
            tfName =target + os.sep + target_prefix +tdxCode + '.xls'
            if(self.ifFileExist(tfName)==False):
                th =Process(target=thread_day2csv_lhb, args=(str_msgQ,td,sourceD,tdxCode,target,target_prefix))
                self.threadList.append(th)
                if((total -i)>=self.MAX_THREAD_NUM):
                    if(len(self.threadList)>=self.MAX_THREAD_NUM):
                        for x in self.threadList:
                            x.daemon=True
                            x.start()#启动进程
                        x.join()#等待进程完成
                        self.threadList.clear()
                else:
                    for x in self.threadList:
                        x.daemon=True
                        x.start()#启动进程
                    x.join()#等待进程完成
                    self.threadList.clear()                    
                        
            else:
                self.EmitMsgToUi("龙虎榜上股票 %s 的数据已经存在"%(tfName))


    def ifPathExist(self,path):
        '''
        检测路径是否存在 如果存在跳过，如果不存在生成
        '''
        if(os.path.exists(path)==False):
            os.mkdir(path)
        else:
            pass

    def ifFileExist(self,fn):
        '''
        检测路径是否存在 如果存在跳过，如果不存在生成
        '''
        if(os.path.exists(fn)==False):
            return False
        else:
            return True         

    def on_btn_lhb_click(self):
        '''
        龙虎榜数据
        '''
        lhb =LHB_LT()
        dayType ="None"
        if(self.rb_5day.isChecked()):
            dayType ="5日"
            df =lhb.getStockLHB(5)
        if(self.rb_10day.isChecked()):
            dayType ="10日"
            df =lhb.getStockLHB(10)
        if(self.rb_30day.isChecked()):
            dayType ="30日"
            df =lhb.getStockLHB(30)
        if(self.rb_60day.isChecked()):
            dayType ="60日"
            df =lhb.getStockLHB(60)
        self.dataLhb =df

        self.model.setHorizontalHeaderLabels(['代码','名称','上榜次数','累积购买额(万)','累积卖出额(万)','净额(万)','买入席位数','卖出席位数'])
        row =0
        if (df is None):
            self.addListViewMessage("读取龙虎榜 %s 没有数据返回"%(dayType))
            return 
        for i in range(0, len(df)):
            # print df.iloc[i]['c1'], df.iloc[i]['c2']
            rowContent =df.iloc[i]
            item=QStandardItem(rowContent['code'])
            self.model.setItem(row,0,item)
            item=QStandardItem(rowContent['name'])
            self.model.setItem(row,1,item)
            item=QStandardItem(str(rowContent['count']))
            self.model.setItem(row,2,item)
            item=QStandardItem(str(rowContent['bamount']))
            self.model.setItem(row,3,item)
            item=QStandardItem(str(rowContent['samount']))
            self.model.setItem(row,4,item)
            item=QStandardItem(str(rowContent['net']))
            self.model.setItem(row,5,item)
            item=QStandardItem(str(rowContent['bcount']))
            self.model.setItem(row,6,item)
            item=QStandardItem(str(rowContent['scount']))
            self.model.setItem(row,7,item)
            row =row +1
        self.tv_lhb.setModel(self.model)                
        self.addListViewMessage("读取龙虎榜 %s 成功"%(dayType))
  
    def callbacklog(self, msg,processInt):
        '''
        # 回调数据输出到信息列表
        '''
        if(len(msg)>0):
            self.addListViewMessage(msg)
        self.setProcessBarPos(processInt)        

 
    def addListViewMessage(self,msg):
        '''
        向信息列表填加信息msg
        '''
        now_time = datetime.datetime.now()
        dateL =now_time.strftime('%H:%M:%S')
        global str_msg
        if(len(msg)>0):
            nMsg ="[%s]:%s"%(dateL,msg)
            self.Test.append(nMsg)
            #设置模型列表视图，加载数据列表
            self.qsL.setStringList(self.Test)
        
    def setProcessBarPos(self,processBar):
        '''
        设置进度条位置
        '''
        self.progressBar.setValue(processBar)

def thread_day2csv_lhb(q,td,source,fn,target,target_prefix):
    '''
    龙虎榜进程 调用函数
    '''
    td =TdxData() 
    if(td.getDbStatus()):
        if(td.day2csv(source, fn, target,target_prefix)==True):
            q.put("成功读取龙虎榜上股票 %s/%s 的数据"%(source,fn))
        else:
            q.put("在通达信的目录中不存在 %s/%s 的数据"%(source,fn))
    else:
        q.put("数据库连接失败")
def thread_day2csv_all(q,td,source,fn,target,target_prefix):
    '''
    读取tdx路径下的文件 导出导数据库和文件xls
    '''
    td =TdxData() 
    if(td.getDbStatus()):
        td.day2csv(source, fn, target,target_prefix) 
        q.put("成功读取%s的数据"%fn)
    else:
        q.put("数据库连接失败")

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = TdxAudTool_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
