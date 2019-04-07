Attribute VB_Name = "baseCall"
Sub FreshDataFromWeb163()
    If Sheet2.Cells.Rows < 30 Then
      rowCnt = Sheet1.Cells.Rows
      For j = 2 To rowCnt
        code = Sheet1.Cells(j, 1)
        col = (j - 1) * 3
        Call getHistPrice(Sheet2, code, col)
      End
    Call GetData
End Sub
Sub getHistPrice(sheet As Worksheet, code, col)
Dim html, i, j, tr, td
Set html = CreateObject("htmlfile")
With CreateObject("msxml2.xmlhttp")
    .Open "GET", "http://quotes.money.163.com/trade/lsjysj_" & code & ".html", False
    .send
    html.body.innerhtml = .responsetext
    'Cells(1, 1) = .responsetext
    sheet.Cells(1, col) = code
    
    For Each tr In html.All.tags("table")(3).Rows
        i = i + 1
        j = 0
        'For Each td In tr.Cells
        '    j = j + 1
        '    Cells(i, j) = td.innerText
        'Next
        sheet.Cells(i + 1, col + 1) = tr.Cells(0).innerText
       ' Cells(i, 2) = tr.Cells(1).innerText
        sheet.Cells(i + 1, col + 2) = tr.Cells(2).innerText '��߼�
        sheet.Cells(i + 1, col + 3) = tr.Cells(3).innerText '��ͼ�
        sheet.Cells(i + 1, col + 3) = tr.Cells(4).innerText '���̼�
    Next
End With
End Sub
Function FillOneRow(url As String, r As Integer) As Integer
    Dim price3, price20 As Integer
    Dim Zs As Double
    Dim cuDate As String
    cuDate = Date
    With CreateObject("msxml2.xmlhttp")
        .Open "GET", url, False
        .send
        sp = Split(.responsetext, "~")
        If UBound(sp) > 3 Then
            FillOneRow = 1
           ' For i = 1 To 56
            '    Cells(r, i + 1).Value = sp(i) '����
            'Next

           cols = Sheet2.Cells.Columns
           Dim j, col As Integer
           For j = 0 To cols
                If Sheet1.Cells(r, 1) = Sheet2.Cells(1, j) Then
                    col = j
                    break
                End
           Next
           
           Zs = sp(4) '����
           Cells(r, 2).Value = sp(1) '����
           Cells(r, 3).Value = sp(33) '��߼�
           Cells(r, 4).Value = sp(3) '��ǰ�۸�
           Cells(r, 5).Value = sp(34) '��ͼ�
           Cells(r, 6).Value = sp(35) '����
           'sp(5) ����
           Cells(r, 7).Value = 100 * (sp(33) - sp(4)) / sp(4) '���%
           Cells(r, 8).Value = 100 * (sp(34) - sp(4)) / sp(4) '���%
           Cells(r, 9).Value = sp(32) '�Ƿ�%
           Cells(r, 10).Value = sp(43) '���%
           Cells(r, 11).Value = 100 * (sp(5) - sp(4)) / sp(4) '����%
           Cells(r, 12).Value = sp(38) '����%
           Cells(r, 13).Value = sp(10) '����
           Cells(r, 14).Value = sp(20) '����
           Cells(r, 15).Value = sp(10) '�ⵥ��
           
           If col >= 1 Then
              price3 = Sheet2.Cells(2 + 3, col)
              price20 = Sheet2.Cells(2 + 20, col)
              price_zd = Sheet2.Cells(2 + 1, col + 1)
              price_zg = Sheet2.Cells(2 + 1, col + 2)
              price_sp = Sheet2.Cells(2 + 1, col + 3)
           End If
           Cells(r, 16).Value = (sp(3) - price3) / sp(3) '3���Ƿ�
           Cells(r, 17).Value = (sp(3) - price3) / sp(3) '20���Ƿ�
           Cells(r, 18).Value = (sp(33) - price_zd) / price_zd '��ֵ
           Cells(r, 19).Value = (sp(33) - price_zg) / price_zg  '��߼۱Ƚ�
           Cells(r, 20).Value = (sp(34) - price_zd) / price_zd '��ͼ۱Ƚ�
           Cells(r, 21).Value = (sp(34) - price_sp) / price_sp '���
           ''''
           Dim zhangDie As Double
           zhangDie = sp(32)
          
           If zhangDie > 0 Then
              '����ʹ�ú�ɫ
                Cells(r, 5).Font.Color = vbRed
                Cells(r, 3).Font.Color = vbRed
            Else
                '�µ�ʹ����ɫ
                Cells(r, 5).Font.Color = &H228B22
                Cells(r, 3).Font.Color = &H228B22
           End If
        Else
            FillOneRow = 0
        End If
    End With
End Function
Sub GetStockHistoryData(sheet As Worksheet, code As String)
'
'http://quotes.money.163.com/trade/lsjysj_000651.html#01b07
'
    sheet.UsedRange.ClearContents
    sheet.Name = code
    With sheet.QueryTables.Add(Connection:= _
        "URL;http://quotes.money.163.com/trade/lsjysj_" & code & ".html#01b07", Destination _
        :=Sheet3.Range("$A$1"))
        .Name = "lsjysj_" & code & ".html#01b07_1"
        .FieldNames = True
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .WebSelectionType = xlSpecifiedTables
        .WebFormatting = xlWebFormattingNone
        .WebTables = "4"
        .WebPreFormattedTextToColumns = True
        .WebConsecutiveDelimitersAsOne = True
        .WebSingleBlockTextImport = False
        .WebDisableDateRecognition = False
        .WebDisableRedirections = False
        .Refresh BackgroundQuery:=False
    End With
End Sub


Sub GetData()
    Dim succeeded As Integer
    Dim url As String
    Dim row As Integer
    Dim code As String
    For row = 2 To Range("A1").CurrentRegion.Rows.Count '�ӵڶ��п�ʼ
        code = Cells(row, 1).Value
        If code <> "" Then
            'url = "http://hq.sinajs.cn/list=sh" & code
            url = "http://qt.gtimg.cn/q=sh" & code '����
            succeeded = FillOneRow(url, row)
            
            If succeeded = 0 Then
                url = "http://qt.gtimg.cn/q=sz" & code '����
                succeeded = FillOneRow(url, row)
            End If
            
            If succeeded = 0 Then
                MsgBox ("��ȡʧ��")
            End If
        End If
    Next
    'Call GetStockHistoryData(Sheet3, "000651")
End Sub
Public TimerEnabled As Boolean
  
  Sub EnableTimer() '��ʼ
    TimerEnabled = True
    StartTimer
  End Sub
  
  Sub DisableTimer() 'ͣ��
    TimerEnabled = False
  End Sub
  
  Sub StartTimer()      'ע��Ĵ�����Ҫ����ģ�鼶
      If TimerEnabled = True Then
        Application.OnTime Now + TimeValue("00:00:01"), "StartTimer" 'ÿ1�����Զ�����һ��
        'FreshDataFromWeb163 '��Ҫÿ�����еĴ���
        shownowtime
      End If
  End Sub

Sub shownowtime()
[E1] = Now() 'ÿ��һ��a1��Ԫ�����ʱ��͸���һ�Σ�����ʵ�����ʵʱ��̬����
End Sub
Sub ��ѡ��1_Click()
    If ��ѡ��1.Value = 1 Then
        MsgBox "hello"
    End If
End Sub

