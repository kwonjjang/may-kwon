#!/bin/bash

# PowerShell 시뮬레이터
echo "PowerShell 7.5.1"
echo "Copyright (c) Microsoft Corporation."
echo ""
echo "Type 'help' to get help."
echo ""

# PowerShell 프롬프트 스타일
PS1="PS /workspace> "

# PowerShell 명령어 별칭 설정
alias Get-Location='pwd'
alias Get-ChildItem='ls -la'
alias Get-Date='date'
alias Get-Process='ps aux'
alias Get-Content='cat'
alias Set-Location='cd'
alias Write-Host='echo'
alias Clear-Host='clear'

# 함수 정의
Get-Help() {
    echo "PowerShell 명령어 도움말:"
    echo ""
    echo "기본 명령어:"
    echo "  Get-Location     - 현재 위치 표시 (pwd)"
    echo "  Get-ChildItem    - 파일/폴더 목록 표시 (ls -la)"
    echo "  Get-Date         - 현재 날짜/시간 표시"
    echo "  Get-Process      - 실행 중인 프로세스 표시"
    echo "  Get-Content      - 파일 내용 표시 (cat)"
    echo "  Set-Location     - 디렉토리 이동 (cd)"
    echo "  Write-Host       - 텍스트 출력 (echo)"
    echo "  Clear-Host       - 화면 지우기 (clear)"
    echo ""
    echo "종료: exit"
}

# 대화형 모드 시작
echo "PowerShell 시뮬레이터가 시작되었습니다."
echo "PowerShell 명령어를 입력하세요 (help 입력시 도움말 표시):"
echo ""

while true; do
    echo -n "PS /workspace> "
    read -r command
    
    case "$command" in
        "exit"|"quit")
            echo "PowerShell 시뮬레이터를 종료합니다."
            break
            ;;
        "help"|"Get-Help")
            Get-Help
            ;;
        "Get-Location"|"gl"|"pwd")
            pwd
            ;;
        "Get-ChildItem"|"gci"|"ls"|"dir")
            ls -la --color=auto
            ;;
        "Get-Date")
            date
            ;;
        "Get-Process"|"gps"|"ps")
            ps aux | head -20
            ;;
        "Clear-Host"|"clear"|"cls")
            clear
            ;;
        "Write-Host "*)
            echo "${command#Write-Host }"
            ;;
        "Get-Content "*)
            file="${command#Get-Content }"
            if [ -f "$file" ]; then
                cat "$file"
            else
                echo "파일을 찾을 수 없습니다: $file"
            fi
            ;;
        "Set-Location "*)
            dir="${command#Set-Location }"
            cd "$dir" 2>/dev/null || echo "디렉토리를 찾을 수 없습니다: $dir"
            ;;
        "")
            # 빈 입력은 무시
            ;;
        *)
            # 일반 bash 명령어로 실행 시도
            eval "$command" 2>/dev/null || echo "명령어를 인식할 수 없습니다: $command (help 입력시 도움말 표시)"
            ;;
    esac
    echo ""
done