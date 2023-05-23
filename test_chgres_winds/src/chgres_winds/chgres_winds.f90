 subroutine main(geolon_s,geolat_s,geolon_w,geolat_w,u_s,v_s,u_w,v_w,ud,vd)
 use omp_lib
 use, intrinsic :: ieee_arithmetic
 implicit none
 real(kind=8), dimension(:,:),   intent(IN)    :: geolon_s,geolat_s !(nlon,nlat)
 real(kind=8), dimension(:,:,:), intent(IN)    :: u_s,v_s
 real(kind=8), dimension(:,:,:), intent(INOUT) :: ud
 real(kind=8), dimension(:,:),   intent(IN)    :: geolon_w,geolat_w
 real(kind=8), dimension(:,:,:), intent(IN)    :: u_w,v_w
 real(kind=8), dimension(:,:,:), intent(INOUT) :: vd
 real(kind=8) :: inner_prod
 real(kind=8), dimension(2):: p1,p2,p3
 real(kind=8), dimension(3):: e1,e2,ex,ey
 integer :: i,j,k
 integer :: is,ie,js,je,ks,ke
 real(kind=8), parameter:: pi=4.D0*DATAN(1.D0)
 real(kind=8), parameter:: deg2rad=pi/180.D0
 real(kind=8), parameter:: rad2deg=180.D0/pi
 real(kind=8), parameter:: r360=360.D0

 is = lbound(ud, dim=1)
 ie = ubound(ud, dim=1)
 js = lbound(vd, dim=2)
 je = ubound(vd, dim=2)
 ks = lbound(ud, dim=3)
 ke = ubound(ud, dim=3)

 write(*,*) "is =",is
 write(*,*) "ie =",ie
 write(*,*) "js =",js
 write(*,*) "je =",je

 write(*,*) "geolon_s(ie+1,1)",geolon_s(ie+1,1),ie+1
 write(*,*) "geolon_s(1,1)",geolon_s(1,1)
 write(*,*) "deg2rad",deg2rad

!$OMP parallel do default(none) &
!$OMP          shared(is,ie,js,je,ks,ke,geolon_s,geolat_s,geolon_w,geolat_w,ud,vd,u_s,v_s,u_w,v_w) &
!$OMP          private(p1,p2,p3,e1,e2,ex,ey)
 do k=ks,ke
   !write(*,*) "k=",k
   do j=js,je+1 !lats
     do i=is,ie !lons
       p1(1) = geolon_s(i,  j)*deg2rad
       p1(2) = geolat_s(i,  j)*deg2rad
       p2(1) = geolon_s(i+1,j)*deg2rad
       p2(2) = geolat_s(i+1,j)*deg2rad
       call mid_pt_sphere(p1, p2, p3)
       call get_unit_vect2(p1, p2, e1)
       call get_latlon_vector(p3, ex, ey)
       ud(i,j,k) = u_s(i,j,k)*inner_prod(e1,ex) + v_s(i,j,k)*inner_prod(e1,ey)
       if ( abs(ud(i,j,k) - 12.8145490901456) .le. 0.000001) then
         write(*,*) "test:i,j,k=",i,j,k
         write(*,*) "ud(i,j,k)",ud(i,j,k)
       endif
       !if (i .eq. 1 .and. j .eq. 1 .and. k .eq. 1) then
       if (i .eq. 327+1 .and. j .eq. 208+1 .and. k .eq. 68+2) then
         write(*,*) "i,j,k=",i,j,k
         write(*,*) "p1=",p1(1)*rad2deg,p1(2)*rad2deg
         write(*,*) "p2=",p2(1)*rad2deg,p2(2)*rad2deg
         write(*,*) "p3=",p3(1)*rad2deg,p3(2)*rad2deg
         write(*,*) "e1=",e1
         write(*,*) "ex=",ex
         write(*,*) "ey=",ey
         write(*,*) "inner_prod(e1,ex)",inner_prod(e1,ex)
         write(*,*) "inner_prod(e1,ey)",inner_prod(e1,ey)
         write(*,*) "u_s(i,j,k)",u_s(i,j,k)
         write(*,*) "v_s(i,j,k)",v_s(i,j,k)
         write(*,*) "ud(i,j,k)",ud(i,j,k)
       end if
       if ( isnan(ud(i,j,k))) then
         write(*,*) "NaN at i,j,k",i,j,k
         stop
       end if
     enddo
   enddo
   do j=js,je
     do i=is,ie+1
       p1(1) = geolon_w(i,j  )*deg2rad
       p1(2) = geolat_w(i,j  )*deg2rad
       p2(1) = geolon_w(i,j+1)*deg2rad
       p2(2) = geolat_w(i,j+1)*deg2rad
       call mid_pt_sphere(p1, p2, p3)
       call get_unit_vect2(p1, p2, e2)
       call get_latlon_vector(p3, ex, ey)
       vd(i,j,k) = u_w(i,j,k)*inner_prod(e2,ex) + v_w(i,j,k)*inner_prod(e2,ey)
       if ( isnan(vd(i,j,k))) then
         write(*,*) "NaN at i,j,k",i,j,k
         stop
       end if
     enddo
   enddo
 enddo

 return
 end subroutine main

   real*8 function inner_prod(v1, v2)
       real(kind=8),intent(in):: v1(3), v2(3)
       real(kind=16) :: vp1(3), vp2(3), prod16
       integer k

         do k=1,3
            vp1(k) = real(v1(k),kind=16)
            vp2(k) = real(v2(k),kind=16)
         enddo
         prod16 = vp1(1)*vp2(1) + vp1(2)*vp2(2) + vp1(3)*vp2(3)
         inner_prod = prod16

  end function inner_prod

 subroutine mid_pt_sphere(p1, p2, pm)
 implicit none
      real(kind=8) , intent(IN)  :: p1(2), p2(2)
      real(kind=8) , intent(OUT) :: pm(2)
!------------------------------------------
      real(kind=8) e1(3), e2(3), e3(3)

      call latlon2xyz(p1, e1)
      call latlon2xyz(p2, e2)
      call mid_pt3_cart(e1, e2, e3)
      call cart_to_latlon(1, e3, pm(1), pm(2))

 end subroutine mid_pt_sphere

 subroutine get_unit_vect2( e1, e2, uc )
 implicit none
   real(kind=8), intent(in) :: e1(2), e2(2)
   real(kind=8), intent(out):: uc(3) !< unit vector e1--->e2
! Local:
   real(kind=8), dimension(3):: pc, p1, p2, p3

! RIGHT_HAND system:
   call latlon2xyz(e1, p1)
   call latlon2xyz(e2, p2)

   call mid_pt3_cart(p1, p2,  pc)
   call vect_cross(p3, p2, p1)
   call vect_cross(uc, pc, p3)
   call normalize_vect( uc )

 end subroutine get_unit_vect2

 subroutine get_latlon_vector(pp, elon, elat)
 implicit none
 real(kind=8), intent(IN)  :: pp(2)
 real(kind=8), intent(OUT) :: elon(3), elat(3)

         elon(1) = -SIN(pp(1))
         elon(2) =  COS(pp(1))
         elon(3) =  0.0
         elat(1) = -SIN(pp(2))*COS(pp(1))
         elat(2) = -SIN(pp(2))*SIN(pp(1))
!!! RIGHT_HAND
         elat(3) =  COS(pp(2))
! Left-hand system needed to be consistent with rest of the codes
!        elat(3) = -COS(pp(2))

 end subroutine get_latlon_vector

!-----------------------------------------------------------------------

!>@brief The subroutine 'normalize_vect' makes 'e' a unit vector.
 subroutine normalize_vect(e)
 implicit none

 real(kind=8), intent(inout):: e(3)
 real(kind=16):: pdot
 integer k

    pdot = e(1)**2 + e(2)**2 + e(3)**2
    pdot = sqrt( pdot )

    do k=1,3
       e(k) = e(k) / pdot
    enddo

 end subroutine normalize_vect

!>@brief The subroutine 'vect_cross performs cross products
!! of 3D vectors: e = P1 X P2
 subroutine vect_cross(e, p1, p2)
 implicit none
 real(kind=8), intent(in) :: p1(3), p2(3)
 real(kind=8), intent(out):: e(3)

      e(1) = p1(2)*p2(3) - p1(3)*p2(2)
      e(2) = p1(3)*p2(1) - p1(1)*p2(3)
      e(3) = p1(1)*p2(2) - p1(2)*p2(1)

 end subroutine vect_cross

!>@brief The subroutine 'latlon2xyz' maps (lon, lat) to (x,y,z)
 subroutine latlon2xyz(p, e, id)
 implicit none

 real(kind=8), intent(in) :: p(2)
 real(kind=8), intent(out):: e(3)
 integer, optional, intent(in):: id !< id=0 do nothing; id=1, right_hand

 integer n
 real(kind=16):: q(2)
 real(kind=16):: e1, e2, e3

 logical, save       :: first_time = .true.
 integer, save       :: id_latlon

    do n=1,2
       q(n) = p(n)
    enddo

    e1 = cos(q(2)) * cos(q(1))
    e2 = cos(q(2)) * sin(q(1))
    e3 = sin(q(2))
!-----------------------------------
! Truncate to the desired precision:
!-----------------------------------
    e(1) = e1
    e(2) = e2
    e(3) = e3

 end subroutine latlon2xyz



 subroutine mid_pt3_cart(p1, p2, e)
 implicit none
       real(kind=8), intent(IN)  :: p1(3), p2(3)
       real(kind=8), intent(OUT) :: e(3)
!
       real(kind=16):: q1(3), q2(3)
       real(kind=16):: dd, e1, e2, e3
       integer k

       do k=1,3
          q1(k) = p1(k)
          q2(k) = p2(k)
       enddo

       e1 = q1(1) + q2(1)
       e2 = q1(2) + q2(2)
       e3 = q1(3) + q2(3)

       dd = sqrt( e1**2 + e2**2 + e3**2 )
       e1 = e1 / dd
       e2 = e2 / dd
       e3 = e3 / dd

       e(1) = e1
       e(2) = e2
       e(3) = e3

 end subroutine mid_pt3_cart

 subroutine cart_to_latlon(np, q, xs, ys)
 implicit none
! vector version of cart_to_latlon1
  integer, intent(in):: np
  real(kind=8), intent(inout):: q(3,np)
  real(kind=8), intent(inout):: xs(np), ys(np)
! local
  real(kind=8), parameter:: esl=1.d-10
  real(kind=8), parameter:: pi=4.D0*DATAN(1.D0)
  real(kind=16):: p(3)
  real(kind=16):: dist, lat, lon
  integer i,k

  do i=1,np
     do k=1,3
        p(k) = q(k,i)
     enddo
     dist = sqrt(p(1)**2 + p(2)**2 + p(3)**2)
     do k=1,3
        p(k) = p(k) / dist
     enddo

     if ( (abs(p(1))+abs(p(2)))  < esl ) then
          lon = real(0.,kind=16)
     else
          lon = atan2( p(2), p(1) )   ! range [-pi,pi]
     endif

     if ( lon < 0.) lon = real(2.,kind=16)*pi + lon
! RIGHT_HAND system:
     lat = asin(p(3))

     xs(i) = lon
     ys(i) = lat
! q Normalized:
     do k=1,3
        q(k,i) = p(k)
     enddo
  enddo

 end  subroutine cart_to_latlon
