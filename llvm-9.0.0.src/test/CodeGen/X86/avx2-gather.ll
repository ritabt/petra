; NOTE: Assertions have been autogenerated by utils/update_llc_test_checks.py
; RUN: llc < %s -mtriple=i686-unknown-unknown -mattr=+avx2 | FileCheck %s --check-prefix=X32
; RUN: llc < %s -mtriple=x86_64-unknown-unknown -mattr=+avx2 | FileCheck %s --check-prefix=X64

declare <4 x float> @llvm.x86.avx2.gather.d.ps(<4 x float>, i8*,
                      <4 x i32>, <4 x float>, i8) nounwind readonly

define <4 x float> @test_x86_avx2_gather_d_ps(i8* %a1, <4 x i32> %idx, <4 x float> %mask) {
; X32-LABEL: test_x86_avx2_gather_d_ps:
; X32:       # %bb.0:
; X32-NEXT:    movl {{[0-9]+}}(%esp), %eax
; X32-NEXT:    vxorps %xmm2, %xmm2, %xmm2
; X32-NEXT:    vgatherdps %xmm1, (%eax,%xmm0,2), %xmm2
; X32-NEXT:    vmovaps %xmm2, %xmm0
; X32-NEXT:    retl
;
; X64-LABEL: test_x86_avx2_gather_d_ps:
; X64:       # %bb.0:
; X64-NEXT:    vxorps %xmm2, %xmm2, %xmm2
; X64-NEXT:    vgatherdps %xmm1, (%rdi,%xmm0,2), %xmm2
; X64-NEXT:    vmovaps %xmm2, %xmm0
; X64-NEXT:    retq
  %res = call <4 x float> @llvm.x86.avx2.gather.d.ps(<4 x float> undef,
                            i8* %a1, <4 x i32> %idx, <4 x float> %mask, i8 2) ;
  ret <4 x float> %res
}

declare <2 x double> @llvm.x86.avx2.gather.d.pd(<2 x double>, i8*,
                      <4 x i32>, <2 x double>, i8) nounwind readonly

define <2 x double> @test_x86_avx2_gather_d_pd(i8* %a1, <4 x i32> %idx, <2 x double> %mask) {
; X32-LABEL: test_x86_avx2_gather_d_pd:
; X32:       # %bb.0:
; X32-NEXT:    movl {{[0-9]+}}(%esp), %eax
; X32-NEXT:    vxorpd %xmm2, %xmm2, %xmm2
; X32-NEXT:    vgatherdpd %xmm1, (%eax,%xmm0,2), %xmm2
; X32-NEXT:    vmovapd %xmm2, %xmm0
; X32-NEXT:    retl
;
; X64-LABEL: test_x86_avx2_gather_d_pd:
; X64:       # %bb.0:
; X64-NEXT:    vxorpd %xmm2, %xmm2, %xmm2
; X64-NEXT:    vgatherdpd %xmm1, (%rdi,%xmm0,2), %xmm2
; X64-NEXT:    vmovapd %xmm2, %xmm0
; X64-NEXT:    retq
  %res = call <2 x double> @llvm.x86.avx2.gather.d.pd(<2 x double> undef,
                            i8* %a1, <4 x i32> %idx, <2 x double> %mask, i8 2) ;
  ret <2 x double> %res
}

declare <8 x float> @llvm.x86.avx2.gather.d.ps.256(<8 x float>, i8*,
                      <8 x i32>, <8 x float>, i8) nounwind readonly

define <8 x float> @test_x86_avx2_gather_d_ps_256(i8* %a1, <8 x i32> %idx, <8 x float> %mask) {
; X32-LABEL: test_x86_avx2_gather_d_ps_256:
; X32:       # %bb.0:
; X32-NEXT:    movl {{[0-9]+}}(%esp), %eax
; X32-NEXT:    vxorps %xmm2, %xmm2, %xmm2
; X32-NEXT:    vgatherdps %ymm1, (%eax,%ymm0,4), %ymm2
; X32-NEXT:    vmovaps %ymm2, %ymm0
; X32-NEXT:    retl
;
; X64-LABEL: test_x86_avx2_gather_d_ps_256:
; X64:       # %bb.0:
; X64-NEXT:    vxorps %xmm2, %xmm2, %xmm2
; X64-NEXT:    vgatherdps %ymm1, (%rdi,%ymm0,4), %ymm2
; X64-NEXT:    vmovaps %ymm2, %ymm0
; X64-NEXT:    retq
  %res = call <8 x float> @llvm.x86.avx2.gather.d.ps.256(<8 x float> undef,
                            i8* %a1, <8 x i32> %idx, <8 x float> %mask, i8 4) ;
  ret <8 x float> %res
}

declare <4 x double> @llvm.x86.avx2.gather.d.pd.256(<4 x double>, i8*,
                      <4 x i32>, <4 x double>, i8) nounwind readonly

define <4 x double> @test_x86_avx2_gather_d_pd_256(i8* %a1, <4 x i32> %idx, <4 x double> %mask) {
; X32-LABEL: test_x86_avx2_gather_d_pd_256:
; X32:       # %bb.0:
; X32-NEXT:    movl {{[0-9]+}}(%esp), %eax
; X32-NEXT:    vxorpd %xmm2, %xmm2, %xmm2
; X32-NEXT:    vgatherdpd %ymm1, (%eax,%xmm0,8), %ymm2
; X32-NEXT:    vmovapd %ymm2, %ymm0
; X32-NEXT:    retl
;
; X64-LABEL: test_x86_avx2_gather_d_pd_256:
; X64:       # %bb.0:
; X64-NEXT:    vxorpd %xmm2, %xmm2, %xmm2
; X64-NEXT:    vgatherdpd %ymm1, (%rdi,%xmm0,8), %ymm2
; X64-NEXT:    vmovapd %ymm2, %ymm0
; X64-NEXT:    retq
  %res = call <4 x double> @llvm.x86.avx2.gather.d.pd.256(<4 x double> undef,
                            i8* %a1, <4 x i32> %idx, <4 x double> %mask, i8 8) ;
  ret <4 x double> %res
}

define <2 x i64> @test_mm_i32gather_epi32(i32 *%a0, <2 x i64> %a1) {
; X32-LABEL: test_mm_i32gather_epi32:
; X32:       # %bb.0:
; X32-NEXT:    movl {{[0-9]+}}(%esp), %eax
; X32-NEXT:    vpcmpeqd %xmm2, %xmm2, %xmm2
; X32-NEXT:    vpxor %xmm1, %xmm1, %xmm1
; X32-NEXT:    vpgatherdd %xmm2, (%eax,%xmm0,2), %xmm1
; X32-NEXT:    vmovdqa %xmm1, %xmm0
; X32-NEXT:    retl
;
; X64-LABEL: test_mm_i32gather_epi32:
; X64:       # %bb.0:
; X64-NEXT:    vpcmpeqd %xmm2, %xmm2, %xmm2
; X64-NEXT:    vpxor %xmm1, %xmm1, %xmm1
; X64-NEXT:    vpgatherdd %xmm2, (%rdi,%xmm0,2), %xmm1
; X64-NEXT:    vmovdqa %xmm1, %xmm0
; X64-NEXT:    retq
  %arg0 = bitcast i32 *%a0 to i8*
  %arg1 = bitcast <2 x i64> %a1 to <4 x i32>
  %mask = bitcast <2 x i64> <i64 -1, i64 -1> to <4 x i32>
  %call = call <4 x i32> @llvm.x86.avx2.gather.d.d(<4 x i32> zeroinitializer, i8* %arg0, <4 x i32> %arg1, <4 x i32> %mask, i8 2)
  %bc = bitcast <4 x i32> %call to <2 x i64>
  ret <2 x i64> %bc
}
declare <4 x i32> @llvm.x86.avx2.gather.d.d(<4 x i32>, i8*, <4 x i32>, <4 x i32>, i8) nounwind readonly

define <2 x double> @test_mm_i32gather_pd(double *%a0, <2 x i64> %a1) {
; X32-LABEL: test_mm_i32gather_pd:
; X32:       # %bb.0:
; X32-NEXT:    movl {{[0-9]+}}(%esp), %eax
; X32-NEXT:    vpcmpeqd %xmm2, %xmm2, %xmm2
; X32-NEXT:    vxorpd %xmm1, %xmm1, %xmm1
; X32-NEXT:    vgatherdpd %xmm2, (%eax,%xmm0,2), %xmm1
; X32-NEXT:    vmovapd %xmm1, %xmm0
; X32-NEXT:    retl
;
; X64-LABEL: test_mm_i32gather_pd:
; X64:       # %bb.0:
; X64-NEXT:    vpcmpeqd %xmm2, %xmm2, %xmm2
; X64-NEXT:    vxorpd %xmm1, %xmm1, %xmm1
; X64-NEXT:    vgatherdpd %xmm2, (%rdi,%xmm0,2), %xmm1
; X64-NEXT:    vmovapd %xmm1, %xmm0
; X64-NEXT:    retq
  %arg0 = bitcast double *%a0 to i8*
  %arg1 = bitcast <2 x i64> %a1 to <4 x i32>
  %cmp = fcmp oeq <2 x double> zeroinitializer, zeroinitializer
  %sext = sext <2 x i1> %cmp to <2 x i64>
  %mask = bitcast <2 x i64> %sext to <2 x double>
  %res = call <2 x double> @llvm.x86.avx2.gather.d.pd(<2 x double> zeroinitializer, i8* %arg0, <4 x i32> %arg1, <2 x double> %mask, i8 2)
  ret <2 x double> %res
}

@x = global [1024 x float] zeroinitializer, align 16

define <4 x float> @gather_global(<4 x i64>, i32* nocapture readnone) {
; X32-LABEL: gather_global:
; X32:       # %bb.0:
; X32-NEXT:    vpcmpeqd %xmm2, %xmm2, %xmm2
; X32-NEXT:    vxorps %xmm1, %xmm1, %xmm1
; X32-NEXT:    vgatherqps %xmm2, x(,%ymm0,4), %xmm1
; X32-NEXT:    vmovaps %xmm1, %xmm0
; X32-NEXT:    vzeroupper
; X32-NEXT:    retl
;
; X64-LABEL: gather_global:
; X64:       # %bb.0:
; X64-NEXT:    vpcmpeqd %xmm2, %xmm2, %xmm2
; X64-NEXT:    vxorps %xmm1, %xmm1, %xmm1
; X64-NEXT:    vgatherqps %xmm2, x(,%ymm0,4), %xmm1
; X64-NEXT:    vmovaps %xmm1, %xmm0
; X64-NEXT:    vzeroupper
; X64-NEXT:    retq
  %3 = tail call <4 x float> @llvm.x86.avx2.gather.q.ps.256(<4 x float> zeroinitializer, i8* bitcast ([1024 x float]* @x to i8*), <4 x i64> %0, <4 x float> <float 0xFFFFFFFFE0000000, float 0xFFFFFFFFE0000000, float 0xFFFFFFFFE0000000, float 0xFFFFFFFFE0000000>, i8 4)
  ret <4 x float> %3
}
declare <4 x float> @llvm.x86.avx2.gather.q.ps.256(<4 x float>, i8*, <4 x i64>, <4 x float>, i8)
