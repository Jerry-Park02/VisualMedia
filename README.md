# VisualMedia

#키보드 입력에 따라 joint_ndx의 숫자를 바꿀 수 있도록 설정

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    joint_1dx = -3
                elif event.key == pygame.K_w:
                    joint_1dx = 3

이는 1,2,3,4 모두 마찬가지

+) Rmat에 투입할 예정인 grab변수를 while문을 이용해 조정

                elif event.key == pygame.K_SPACE:
                    while grab <= 25:
                        grab += 1


w만큼 세로로 이동하고 다시 h/2로 이동시켜 로봇 팔 일부를 위로 올림

        H3 = H21 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        x, y = H3[0,2], H3[1,2]
        
해당 점에 점 찍고
        
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        
이 점은 딱 정중앙점, 그러나 우리가 구해야 할 점은 사각형의 꼭짓점
Rmat(joint_3) @ Tmat(0, -h/2)'''을 이용 회전, 중앙
        
        H31 = H3 @ Rmat(joint_3) @ Tmat(0, -h/2)
        draw(X, H31, screen, (0,0, 200))

H4는 집게의 중심
Rmat(90 + joint_4) -를 통해 joint4로 추가적으로 90도 이동
Tmat(-w1/2, -h1/2) - 중심을 그에 따라 이동
        
        H4 = H31 @ Tmat(w,h/2) @ Rmat(90 + joint_4) @Tmat(-w1/2, -h1/2)
        draw(Y, H4, screen, (0,0, 200))
        

H4 @Tmat(grab,0)
grab만큼 이동
spacebar를 누르는 동안 25만큼 커진 상태 유지
키에서 손 뗴면 다시 복귀
        
        H41 = H4 @Tmat(grab,0) @ Rmat(-90)
        draw(Z,H41, screen, (0,0, 200))
        
마찬가지 로직
        
        H42 = H4 @Tmat(-grab,0) @ Rmat(-90) @Tmat(0,w1 - h2) 
        draw(Z,H42, screen, (0,0, 200))
        

유튜브 링크 참조
<https://www.youtube.com/watch?v=HzriY9Tm3eQ>


```
