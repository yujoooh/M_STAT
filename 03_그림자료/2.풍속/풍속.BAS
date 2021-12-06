Sub Main

Dim Grapher As Object
Set Grapher = CreateObject("Grapher.Application")
Grapher.Visible = False
Set 파고grf = Grapher.Documents.Open(CurDir()+"\풍속.grf")
Set Graph1 = 파고grf.Shapes.Item(1)

Open CurDir()+"\풍속.inp" For Input As #2
Open CurDir()+"\NUM.inp" For Input As #3
While Not EOF(2)
   Line Input #2, Outfile
   Line Input #3, NUM
   Debug.Print Outfile
   Set 모델 = Graph1.Plots.Item(1)
   모델.worksheet = CurDir()+"\그림\"+Trim(Outfile)+".dat"
   Set 관측 = Graph1.Plots.Item(2)
   관측.worksheet = CurDir()+"\그림\"+Trim(Outfile)+".dat"
   Set 편차 = Graph1.Plots.Item(3)
   편차.worksheet = CurDir()+"\그림\"+Trim(Outfile)+".dat"

   'Export objects to specified file
   '파고grf.Export2(CurDir()+"\"+TRIM(NUM)+"_"+Trim(Outfile)+".gif",False,"ColorDepth=8;ColorReductionMethod=5;ExportImageFormatIndexed8=1;HDPI=150;Height=352;KeepAspect=1;VDPI=150;Width=1073",True,"gif")
   파고grf.Export2(CurDir()+"\"+TRIM(NUM)+"_"+Trim(Outfile)+".png",False,"ColorDepth=8;ColorReductionMethod=5;ExportImageFormatIndexed8=1;HDPI=200;Height=383;KeepAspect=1;VDPI=200;Width=1031",True,"png")
Wend
End Sub
