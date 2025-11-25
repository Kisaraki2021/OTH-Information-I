let questions = [];
let currentIndex = 0;
let correctCount = 0;
let answeredCount = 0;
let answered = false;
let correctAnswerIndex = -1;

// 問題データを読み込む
async function loadQuestions() {
    try {
        const response = await fetch('test.json');
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

// 問題を更新
function updateQuestion() {
    if (questions.length === 0) return;

    const question = questions[currentIndex];
    document.getElementById('question-text').textContent = question.question;

    // 選択肢を生成
    const choices = generateChoices(question);
    const choiceButtons = document.querySelectorAll('.choice-btn');

    choiceButtons.forEach((btn, index) => {
        btn.textContent = choices[index];
        btn.className = 'choice-btn';
        btn.disabled = false;
    });

    // 結果エリアをリセット
    document.getElementById('result').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('choices').style.display = 'grid';

    answered = false;
}

// 選択肢を生成
function generateChoices(currentQuestion) {
    const correctAnswer = currentQuestion.answer;
    const choices = [correctAnswer];

    // 他の問題から不正解の選択肢を取得
    const otherAnswers = questions
        .filter(q => q.answer !== correctAnswer)
        .map(q => q.answer);

    shuffleArray(otherAnswers);

    // 3つの不正解選択肢を追加
    for (let i = 0; i < 3 && i < otherAnswers.length; i++) {
        choices.push(otherAnswers[i]);
    }

    // 選択肢をシャッフル
    shuffleArray(choices);

    // 正解の位置を記録
    correctAnswerIndex = choices.indexOf(correctAnswer);

    return choices;
}

// 回答を選択
function selectAnswer(index) {
    if (answered) return;
    answered = true;
    answeredCount++;

    const choiceButtons = document.querySelectorAll('.choice-btn');
    const isCorrect = index === correctAnswerIndex;

    // 全ボタンを無効化
    choiceButtons.forEach(btn => btn.disabled = true);

    // 正解・不正解の表示
    if (isCorrect) {
        correctCount++;
        choiceButtons[index].classList.add('correct');
        document.getElementById('result-text').textContent = '⭕ 正解！';
        document.getElementById('result-text').className = 'correct-text';
    } else {
        choiceButtons[index].classList.add('incorrect');
        choiceButtons[correctAnswerIndex].classList.add('correct');
        document.getElementById('result-text').textContent = '❌ 不正解';
        document.getElementById('result-text').className = 'incorrect-text';
    }

    document.getElementById('correct-answer').textContent =
        `正解: ${questions[currentIndex].answer}`;
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
    document.getElementById('choices').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';

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
    document.getElementById('choices').style.display = 'grid';

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

// 初期化
document.addEventListener('DOMContentLoaded', loadQuestions);
