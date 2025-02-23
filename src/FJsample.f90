module FJsample
   use FJsample__types, only: WP, WC, C_DOUBLE, C_DOUBLE_COMPLEX, C_INT
   use FJsample__jack, only: Complement, jackError
   implicit none(external)
   private

   public :: say_hello, Complement, jackError, C_DOUBLE, C_DOUBLE_COMPLEX, C_INT
contains
   subroutine say_hello
      print *, "Hello, FJsample!"
   end subroutine say_hello
end module FJsample
