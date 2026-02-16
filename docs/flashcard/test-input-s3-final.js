let questions = [];
let currentIndex = 0;
let correctCount = 0;
let answeredCount = 0;
let answered = false;

// 問題データを読み込む
async function loadQuestions() {
    try {
        const response = await fetch('test-s3-final.json');
        questions = await response.json();
        shuffleArray(questions);
        updateQuestion();
        updateProgress();
        updateScore();
    } catch (error) {
        console.error('問題の読み込みに失敗しました:', error);
    }
}

// 配列をシャッフル
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// 文字列を正規化（全角半角、大文字小文字、記号などを統一）
function normalizeString(str) {
    if (!str) return '';

    // 全角英数字を半角に変換
    let normalized = str.replace(/[Ａ-Ｚａ-ｚ０-９]/g, function (s) {
        return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);
    });

    // 全角スペースを半角に
    normalized = normalized.replace(/　/g, ' ');

    // 小文字に統一
    normalized = normalized.toLowerCase();

    // 前後の空白を削除
    normalized = normalized.trim();

    // 連続する空白を1つに
    normalized = normalized.replace(/\s+/g, ' ');

    // 一般的な表記ゆれを統一
    normalized = normalized
        .replace(/ー/g, '-')        // 長音符を半角ハイフンに
        .replace(/−/g, '-')         // 全角マイナスを半角に
        .replace(/／/g, '/')        // 全角スラッシュを半角に
        .replace(/（/g, '(')        // 全角括弧を半角に
        .replace(/）/g, ')')
        .replace(/[、，]/g, ',')    // 読点をカンマに
        .replace(/[。．]/g, '.')    // 句点をピリオドに
        ;

    return normalized;
}

// 回答が正解かどうかを判定
function checkAnswer(userAnswer, question) {
    const normalizedUser = normalizeString(userAnswer);
    const normalizedCorrect = normalizeString(question.answer);

    // メイン回答との一致
    if (normalizedUser === normalizedCorrect) {
        return true;
    }

    // 代替回答との一致
    if (question.alternativeAnswers && question.alternativeAnswers.length > 0) {
        for (const alt of question.alternativeAnswers) {
            if (normalizedUser === normalizeString(alt)) {
                return true;
            }
        }
    }

    return false;
}

// 問題を更新
function updateQuestion() {
    if (questions.length === 0) return;

    const question = questions[currentIndex];
    document.getElementById('question-text').textContent = question.question;

    // 入力欄をリセット
    const input = document.getElementById('answer-input');
    input.value = '';
    input.disabled = false;
    input.focus();

    document.getElementById('submit-btn').disabled = false;
    document.getElementById('submit-btn').style.display = 'inline-block';

    // 結果エリアをリセット
    document.getElementById('result').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';

    answered = false;
}

// 回答を送信
function submitAnswer() {
    if (answered) return;

    const userAnswer = document.getElementById('answer-input').value;
    if (!userAnswer.trim()) {
        alert('答えを入力してください');
        return;
    }

    answered = true;
    answeredCount++;

    const question = questions[currentIndex];
    const isCorrect = checkAnswer(userAnswer, question);

    // 入力欄を無効化
    document.getElementById('answer-input').disabled = true;
    document.getElementById('submit-btn').disabled = true;

    // 正解・不正解の表示
    if (isCorrect) {
        correctCount++;
        document.getElementById('result-text').textContent = '⭕ 正解！';
        document.getElementById('result-text').className = 'correct-text';
    } else {
        document.getElementById('result-text').textContent = '❌ 不正解';
        document.getElementById('result-text').className = 'incorrect-text';
    }

    document.getElementById('correct-answer').textContent =
        `正解: ${question.answer}`;
    document.getElementById('result').style.display = 'block';

    updateScore();

    // 最後の問題かどうか
    if (currentIndex < questions.length - 1) {
        document.getElementById('next-btn').style.display = 'inline-block';
    } else {
        showFinalResult();
    }
}

// 次の問題へ
function nextQuestion() {
    currentIndex++;
    updateQuestion();
    updateProgress();
}

// 進捗を更新
function updateProgress() {
    document.getElementById('progress').textContent =
        `${currentIndex + 1} / ${questions.length}`;
}

// スコアを更新
function updateScore() {
    document.getElementById('score').textContent =
        `正解: ${correctCount} / ${answeredCount}`;
}

// 最終結果を表示
function showFinalResult() {
    document.getElementById('next-btn').style.display = 'none';
    document.querySelector('.input-area').style.display = 'none';

    const percentage = Math.round((correctCount / questions.length) * 100);
    let message = '';

    if (percentage === 100) {
        message = '🎉 パーフェクト！素晴らしい！';
    } else if (percentage >= 80) {
        message = '👏 よくできました！';
    } else if (percentage >= 60) {
        message = '📚 もう少し復習しましょう！';
    } else {
        message = '💪 頑張って復習しよう！';
    }

    document.getElementById('final-score').innerHTML =
        `${questions.length}問中 ${correctCount}問正解<br>(${percentage}%)<br><br>${message}`;
    document.getElementById('final-result').style.display = 'block';
}

// テストをやり直す
function restartTest() {
    currentIndex = 0;
    correctCount = 0;
    answeredCount = 0;
    answered = false;

    shuffleArray(questions);

    document.getElementById('final-result').style.display = 'none';
    document.querySelector('.input-area').style.display = 'flex';

    updateQuestion();
    updateProgress();
    updateScore();
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

// Enterキーで回答送信
document.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !answered) {
        submitAnswer();
    }
});

// 初期化
document.addEventListener('DOMContentLoaded', loadQuestions);
