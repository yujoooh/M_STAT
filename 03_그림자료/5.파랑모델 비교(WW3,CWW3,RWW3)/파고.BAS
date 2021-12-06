Sub Main

Dim Grapher As Object
Set Grapher = CreateObject("Grapher.Application")
Grapher.Visible = False
Set 파고grf = Grapher.Documents.Open(CurDir()+"\파고.grf")
Set Graph1 = 파고grf.Shapes.Item(1)

Open CurDir()+"\파고.inp" For Input As #2
Open CurDir()+"\NUM.inp" For Input As #3
While Not EOF(2)
   Line Input #2, Outfile
   Line Input #3, NUM
   Debug.Print Outfile
   Set RWW3 = Graph1.Plots.Item(1)
   RWW3.worksheet = CurDir()+"\그림\"+Trim(Outfile)+".dat"
   Set CWW3 = Graph1.Plots.Item(2)
   CWW3.worksheet = CurDir()+"\그림\"+Trim(Outfile)+".dat"
   Set WW3 = Graph1.Plots.Item(3)
   WW3.worksheet = CurDir()+"\그림\"+Trim(Outfile)+".dat"
   Set 관측 = Graph1.Plots.Item(4)
   관측.worksheet = CurDir()+"\그림\"+Trim(Outfile)+".dat"


   'Export objects to specified file
   파고grf.Export2(CurDir()+"\"+Trim(NUM)+"_"+Trim(Outfile)+".png",False,"ColorDepth=8;ColorReductionMethod=5;ExportImageFormatIndexed8=1;HDPI=200;Height=380;KeepAspect=1;VDPI=200;Width=986",True,"png")
Wend
End Sub
