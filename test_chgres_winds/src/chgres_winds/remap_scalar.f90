 subroutine main(ak, bk, ps, zh)
 use omp_lib
 use, intrinsic :: ieee_arithmetic
 implicit none
 real(kind=8), dimension(:),     intent(IN)    ::  ak, bk
 real(kind=8), dimension(:,:),   intent(IN)    ::  ps
 real(kind=8), dimension(:,:,:), intent(IN)    ::  zh
 real(kind=8), dimension(:)     :: pn,gz
 real(kind=8), dimension(:,:)   :: pe0
 real(kind=8), dimension(:,:,:) :: 
 integer :: i,j,k
 integer :: is,ie,js,je,ks,ke
 real(kind=8), parameter:: grav=9.81

 is = lbound(ps, dim=1)
 ie = ubound(ps, dim=1)
 js = lbound(ps, dim=2)
 je = ubound(ps, dim=2)
 ks = lbound(ak, dim=1)
 ke = ubound(ak, dim=1)

 do j=js,je

   do k=1,km+1
     do i=is,ie
       pe0(i,k) = ak(k) + bk(k)*ps(i,j)
       pn0(i,k) = log(pe0(i,k))
     enddo
   enddo

   do i=is,ie
     do k=1,km+1
       pn(k) = pn0(i,k)
       gz(k) = zh(i,j,k)*grav
     enddo


 enddo


 end subroutine main
