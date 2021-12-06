program R_RMSE

character*20 C
real OBS(100000),PRE(100000),DIFF(100000)
real dum,Mean_Obs,Mean_Pre
real R,RMSE,R2,RMSESUM
real sum1,sum2,sum3,sum4
integer i,inum,tnum,RMSECON
character date*18,fname*30

open(2,file='파고.inp')
open(3,file='../파고_cww3.dat')
do
   read(2,*,end=10) fname
   open(21,file='../SUM/'//trim(fname)//'.dat')
   i=1
   j=1
   do
     !read(21,*,end=11) date,OBS(i),PRE(i) !ww3
     read(21,*,end=11) date,OBS(i),dum,PRE(i) !cww3
!     if(.not.(isnan(OBS(i))).and..not.(isnan(PRE(i)))) i=i+1
     if(.not.(isnan(OBS(i))).and..not.(isnan(PRE(i)))) then
     !if(.not.(isnan(OBS(i)))) then
      if(OBS(i).ne.-99. ) i=i+1
	 endif
     j=j+1
   enddo
   11 continue
   close(21)
   close(22)
   
   inum=i-1
   tnum=j-1
   write(99,*) tnum, inum
   Mean_Obs=0. ;   Mean_Pre=0.
   sum1=0. ;   sum2=0. ;   sum3=0. ;   sum4=0.
!CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
!   Mean value
!CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
   do i=1,inum
       Mean_Obs = Mean_Obs + OBS(i)
       Mean_Pre = Mean_Pre + PRE(i)
	   DIFF(i)  = abs(OBS(i) - PRE(i))
   enddo
   Mean_Obs=Mean_Obs/real(inum)
   Mean_Pre=Mean_Pre/real(inum)
!CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
!   Correlation Coefficient
!CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
   R=0.
   R2=0.
   do i=1,inum
       sum1 = sum1 + ( OBS(i) - Mean_Obs )*( PRE(i) - Mean_Pre )
       sum2 = sum2 + ( OBS(i) - Mean_Obs )**2
       sum3 = sum3 + ( PRE(i) - Mean_Pre )**2
   enddo
   R  = sum1 / sqrt(sum2*sum3)
   R2 = R*R
!CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
!   Root mean square error
!CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
   do i=1,inum
       sum4 = sum4 + ( OBS(i) - PRE(i) )**2
   enddo
   RMSE = sqrt(sum4/real(inum))
    write(3,'(1A30,5F12.5)') trim(fname),100.*real(inum)/real(tnum),maxval(DIFF(1:inum)),sum(DIFF(1:inum))/real(inum),R,RMSE
enddo
10 continue
end program