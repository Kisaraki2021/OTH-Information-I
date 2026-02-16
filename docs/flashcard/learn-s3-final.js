let questions = [];
let currentIndex = 0;
let isFlipped = false;

// 問題データを読み込む
async function loadQuestions() {
    try {
        const response = await fetch('questions-s3-final.json');
        questions = await response.json();
        updateCard();
        updateProgress();
    } catch (error) {
        console.error('問題の読み込みに失敗しました:', error);
    }
}

// カードを更新する
function updateCard() {
    if (questions.length === 0) return;

    const question = questions[currentIndex];

    document.getElementById('question-text').textContent = question.question;
    document.getElementById('answer-text').textContent = question.answer;

    const noteElement = document.getElementById('note-text');
    if (question.note && question.note.trim() !== '') {
        noteElement.textContent = question.note;
        noteElement.style.display = 'block';
    } else {
        noteElement.style.display = 'none';
    }

    // カードを表面に戻す
    const card = document.getElementById('card');
    card.classList.remove('flipped');
    isFlipped = false;

    // ボタンの有効/無効を更新
    document.getElementById('prev-btn').disabled = currentIndex === 0;
    document.getElementById('next-btn').disabled = currentIndex === questions.length - 1;
}

// 進捗を更新する
function updateProgress() {
    document.getElementById('progress').textContent =
        `${currentIndex + 1} / ${questions.length}`;
}

// カードをめくる
function flipCard() {
    const card = document.getElementById('card');
    card.classList.toggle('flipped');
    isFlipped = !isFlipped;
}

// 前の問題へ
function prevQuestion() {
    if (currentIndex > 0) {
        currentIndex--;
        updateCard();
        updateProgress();
    }
}

// 次の問題へ
function nextQuestion() {
    if (currentIndex < questions.length - 1) {
        currentIndex++;
        updateCard();
        updateProgress();
    }
}

// シャッフルする
function shuffleQuestions() {
    for (let i = questions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [questions[i], questions[j]] = [questions[j], questions[i]];
    }
    currentIndex = 0;
    updateCard();
    updateProgress();
}

// 最初に戻る
function resetToStart() {
    currentIndex = 0;
    updateCard();
    updateProgress();
}

// ハンバーガーメニューの開閉
function toggleMenu() {
    const btn = document.getElementById('hamburger-btn');
    const menu = document.getElementById('menu-content');
    btn.classList.toggle('active');
    menu.classList.toggle('show');
}

// メニュー外クリックで閉じる
document.addEventListener('click', function (event) {
    const menu = document.getElementById('menu-content');
    const btn = document.getElementById('hamburger-btn');

    if (!menu.contains(event.target) && !btn.contains(event.target)) {
        menu.classList.remove('show');
        btn.classList.remove('active');
    }
});

// キーボード操作
document.addEventListener('keydown', function (event) {
    switch (event.key) {
        case 'ArrowLeft':
            prevQuestion();
            break;
        case 'ArrowRight':
            nextQuestion();
            break;
        case ' ':
        case 'Enter':
            event.preventDefault();
            flipCard();
            break;
    }
});

// 初期化
document.addEventListener('DOMContentLoaded', loadQuestions);
