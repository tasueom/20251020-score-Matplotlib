function checkScore(f) {
    const kor = parseFloat(f.kor.value);
    const eng = parseFloat(f.eng.value);
    const mat = parseFloat(f.mat.value);

    if (isNaN(kor) || kor < 0 || kor > 100) {
        alert("국어 점수는 0~100 사이의 숫자여야 합니다.");
        f.kor.focus();
        return false;
    }
    if (isNaN(eng) || eng < 0 || eng > 100) {
        alert("영어 점수는 0~100 사이의 숫자여야 합니다.");
        f.eng.focus();
        return false;
    }
    if (isNaN(mat) || mat < 0 || mat > 100) {
        alert("수학 점수는 0~100 사이의 숫자여야 합니다.");
        f.mat.focus();
        return false;
    }
    return true;
}
