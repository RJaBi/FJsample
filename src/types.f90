module FJsample__types
   use ISO_C_BINDING, only: C_DOUBLE, C_DOUBLE_COMPLEX, C_INT
   implicit none(external)
   private
   integer, parameter :: dp = C_DOUBLE
   integer, parameter :: dc = C_DOUBLE_COMPLEX

   integer, parameter :: WP = DP
   integer, parameter :: WC = DC

   public :: WP, WC
   ! for the c_wrapper
   public :: C_DOUBLE, C_DOUBLE_COMPLEX, C_INT

end module FJsample__types
