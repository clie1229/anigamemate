@echo off
chcp 65001 >nul
cd /d "C:\Users\forev\anigamemate"
echo ============================================
echo   AnigameMate GitHub 업로드
echo ============================================
echo.
echo 잠시 후 GitHub 로그인 창(브라우저)이 뜹니다.
echo   - clie1229 계정으로 로그인하세요.
echo   - "Authorize"(승인) 버튼을 누르세요.
echo.
echo 업로드 중... (로그인 완료까지 이 창은 기다립니다)
echo.
git push -u origin main > push-log.txt 2>&1
type push-log.txt
echo.
echo ============================================
echo   결과가 push-log.txt 에도 저장되었습니다.
echo   이 창을 닫고 채팅에 "됐어" 라고 알려주세요.
echo ============================================
echo.
pause
