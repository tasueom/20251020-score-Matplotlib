import mysql.connector

# MySQL 기본 연결 설정 (데이터베이스를 지정하지 않고 접속)
base_config = {
    "host": "localhost",   # MySQL 서버 주소 (로컬)
    "user": "root",        # MySQL 계정
    "password": "1234"     # MySQL 비밀번호
}

# 사용할 데이터베이스 이름
DB_NAME = "scoredb"

# 커넥션과 커서 반환하는 함수
def get_conn():
    return mysql.connector.connect(database=DB_NAME, **base_config)

#테이블 생성
def init_db():
    # DB 생성 (없으면 자동 생성)
    conn = mysql.connector.connect(**base_config)
    cur = conn.cursor()
    cur.execute(f"create database if not exists {DB_NAME} default character set utf8mb4")
    conn.commit()
    conn.close()
    
    conn = get_conn()
    cur = conn.cursor()
    #회원 테이블
    cur.execute("""
                CREATE TABLE if not exists scores (
                sid INT PRIMARY KEY AUTO_INCREMENT,
                sname VARCHAR(50) NOT NULL,
                kor INT NOT NULL,
                eng INT NOT NULL,
                mat INT NOT NULL,
                total INT AS (kor + eng + mat) STORED,
                avg_score DECIMAL(5,2) AS (ROUND((kor + eng + mat)/3, 2)) STORED,
                srank INT)
                """)
    conn.commit()
    conn.close()

def insert_score(sname, kor, eng, mat):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
                insert into scores(sname, kor, eng, mat)
                values(%s, %s, %s, %s)
                """,(sname, kor, eng, mat))
    conn.commit()
    conn.close()

def get_all_scores():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
                select
                sname, kor, eng, mat, total, avg_score, srank
                from scores
                """)
    rows = cur.fetchall()
    conn.close()
    return rows