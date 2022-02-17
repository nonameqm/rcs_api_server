# Robot Control System (API-SERVER)
------------
# Introduction
- ROS2 기반의 X-ARM6를 제동하기 위한 관제 시스템(https://candy-muskox-1d3.notion.site/Xarm6-a8a221d2dd0a4a269ad2fb3319a23847) REST_API_SERVER
  - FASTAPI를 통한 API 구현 (Swagger 파일 존재 ip:port/docs)
  - InfluxDB(https://www.influxdata.com/)와 MQTT(https://mqtt.org/) 사용 실시간 데이터 체크 - (https://github.com/nonameqm/robotmqtt_proj)
  - MYSQL을 통해 DB 관리

- Flutter 기반의 크로스 플랫폼 프론트엔드 구현 (https://github.com/nonameqm/flutter_app_rcs)




# How to Install
- python 3.8 이상 필요
- ubuntu 18.04에서 Test를 진행하였음


1. git clone https://github.com/nonameqm/rcs_api_server
2. cd rcs_api_server
3. pip3 install -r require.txt (필수 라이브러리 설)
4. python3 app/main.py



# 프로젝트 디렉토리
- app
  - common - Connection Info 및 상수 파일

  - logic - Application 내 공통 로직 함수 파ㅌ

  - routes - Routing 포함, 실제 rest_api 구현 파트

  - static - 실제 X-ARM6 Method Data 저장 위치

  - main.py - 실행 파일

  - scheme.py - MYSQL 데이터베이스 스키마

  - models.py - Response, Requqest 모델 정의 


# RESTAPI 정리
- routes 폴더
  - auth.py -> RCS 프로그램 로그인 및 등록에 관련된 API (USer, AuthToken  구현)
  - item.py -> Company, Robot, Factory, TestResult 등 각종 시스템에 있는 구현 정리
  - register.py -> 데이터 생성에  관한 API
  - robot.py -> 로봇 ROS와의 통신을 위한 API (Command와 관련된 API는 (https://candy-muskox-1d3.notion.site/command-API-a880979f33e44bb093fdbf24afc543f5) 참조)
  - test.py -> TEST API


- scheme.py
- ![QuickDBD-Free Diagram](https://user-images.githubusercontent.com/48423723/154422342-90450b43-bbda-4c71-8d60-54fbfbc8bdda.png)


+ Get
  + /item/factory_overview/{factory}
    + factory : string - factory_name
    + result : {pass: 0, defection: 0 }    
+ POST
