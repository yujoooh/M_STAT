Sub Main

Dim Grapher As Object
Set Grapher = CreateObject("Grapher.Application")
Grapher.Visible = False
Set SKgrf = Grapher.Documents.Open(CurDir()+"\source\SK.grf")
Set Graph1 = SKgrf.Shapes.Item(1)

Open CurDir()+"\source\SK_GRAPH.inp" For Input As #2
Open CurDir()+"\source\NUM.inp" For Input As #3

While Not EOF(2)
   Line Input #2, Outfile
   Line Input #3, NUM
   Debug.Print Outfile
   Set ¸ðµ¨ = Graph1.Plots.Item(1)
   ¸ðµ¨.worksheet =  CurDir()+"\OUTPUT\GRAPH\"+Trim(Outfile)+".dat"
   Set °üÃø = Graph1.Plots.Item(2)
   °üÃø.worksheet = CurDir()+"\OUTPUT\GRAPH\"+Trim(Outfile)+".dat"

'   Set Text1 = SKgrf.Shapes.Item(3)
'   Text1.Select
'   Text1.text = Trim(Outfile)
'   Text1.Font.face = "¸¼Àº °íµñ"
'   Text1.Font.color = grfColorBlack
'   Text1.Font.Opacity = 100
'   Text1.Font.size = 14
'   Text1.Font.Bold = True
'   Graph1.Select
''   SKgrf.Selection.Align(2,0) - À§Ä¡ÀÌµ¿
''    -> Selection.Align(grfHARight, grfVABottom)
''       grfHARight = 0: none, 1: left, 2: center, 3: right
''       grfVABottom = 0: none, 1: top, 2: center, 3: bottom


   
   'Export objects to specified file
   'ÆÄ°ígrf.Export2(CurDir()+"\"+TRIM(NUM)+"_"+Trim(Outfile)+".gif",False,"ColorDepth=8;ColorReductionMethod=5;ExportImageFormatIndexed8=1;HDPI=150;Height=352;KeepAspect=1;VDPI=150;Width=1073",True,"gif")
   SKgrf.Export2(CurDir()+"\OUTPUT\PNG\SK\"+Trim(NUM)+"_"+Trim(Outfile)+".png",False,"ColorDepth=8;ColorReductionMethod=5;ExportImageFormatIndexed8=1;HDPI=200;Height=243;KeepAspect=1;VDPI=200;Width=1092",True,"png")
Wend
End Sub
