<template>
  <div class="home-page">

    
    <!-- Основной контент -->
    <main class="content">
      <!-- Герой секция -->
      <section class="hero-section">
        <div class="hero-content">
          <h1>Ваш персональный ИИ-помощник всегда на связи</h1>
          <p class="hero-subtitle">Анонимная поддержка, доступная 24/7</p>
          <div class="hero-actions">
            <button class="cta-button primary" @click="scrollToChat">Начать беседу</button>
            <button class="cta-button secondary" @click="scrollToFeatures">Узнать больше</button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card card-1">
            <div class="card-icon">💬</div>
            <p>Анонимный чат</p>
          </div>
          <div class="floating-card card-3">
            <div class="card-icon">📊</div>
            <p>Отслеживание прогресса</p>
          </div>
        </div>
      </section>

      <!-- Секция с чат-интерфейсом -->
      <section class="chat-section" id="chat-section">
        <div class="chat-container">
          <h2>Начните беседу с ИИ-помощник</h2>
          <p class="section-description">Получите мгновенную поддержку в любое время дня и ночи</p>
          <div class="input-container">
            <div class="input-wrapper">
              <input
                v-model="message"
                type="text"
                placeholder="Напишите ваше сообщение..."
                class="chat-input"
                @keypress.enter="startChat"
              />
              <button class="send-button" @click="startChat">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
            <div class="examples">
              <span class="example-text">Попробуйте спросить: </span>
              <span class="example-item" @click="setExample('Как справиться с тревогой?')">Как справиться с тревогой?</span>
              <span class="example-item" @click="setExample('Помогите с бессонницей')">Помогите с бессонницей</span>
              <span class="example-item" @click="setExample('Как улучшить настроение?')">Как улучшить настроение?</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Секция с преимуществами -->
      <section class="features-section" id="features-section">
        <h2>Почему выбирают Serenity?</h2>
        <p class="section-description">Инновационный подход к ментальному здоровью с использованием искусственного интеллекта</p>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#805AD5" stroke-width="2"/>
                <path d="M8 12H16" stroke="#805AD5" stroke-width="2" stroke-linecap="round"/>
                <path d="M12 8V16" stroke="#805AD5" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <h3>Доступность 24/7</h3>
            <p>Получайте помощь в любое время суток, когда вам это необходимо. Не нужно ждать записи к специалисту.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                <path d="M21 16V8.00002C20.9996 7.6493 20.9071 7.30483 20.7315 7.00119C20.556 6.69754 20.3037 6.44539 20 6.27002L13 2.27002C12.696 2.09449 12.3511 2.00208 12 2.00208C11.6489 2.00208 11.304 2.09449 11 2.27002L4 6.27002C3.69626 6.44539 3.44398 6.69754 3.26846 7.00119C3.09294 7.30483 3.00036 7.6493 3 8.00002V16C3.00036 16.3508 3.09294 16.6952 3.26846 16.9989C3.44398 17.3025 3.69626 17.5547 4 17.73L11 21.73C11.304 21.9056 11.6489 21.998 12 21.998C12.3511 21.998 12.696 21.9056 13 21.73L20 17.73C20.3037 17.5547 20.556 17.3025 20.7315 16.9989C20.9071 16.6952 20.9996 16.3508 21 16Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3.27002 6.96002L12 12L20.73 6.96002" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 22.08V12" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3>Конфиденциальность</h3>
            <p>Ваши данные защищены и анонимны. Мы используем end-to-end шифрование для всех ваших бесед.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                <path d="M9 11L12 14L22 4" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M21 12V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H16" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3>Научный подход</h3>
            <p>Методы, основанные на доказательной психологии: КПТ, ACT, mindfulness и других проверенных методиках.</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M19.4 15C19.2669 15.3016 19.2272 15.6362 19.286 15.9606C19.3448 16.285 19.4995 16.5853 19.73 16.82L19.79 16.88C19.976 17.0657 20.1235 17.2862 20.2241 17.5291C20.3248 17.772 20.3766 18.0329 20.3766 18.2965C20.3766 18.5601 20.3248 18.821 20.2241 19.0639C20.1235 19.3068 19.976 19.5273 19.79 19.713C19.6043 19.899 19.3838 20.0465 19.1409 20.1471C18.898 20.2478 18.6371 20.2996 18.3735 20.2996C18.1099 20.2996 17.849 20.2478 17.6061 20.1471C17.3632 20.0465 17.1427 19.899 16.957 19.713L16.897 19.653C16.6623 19.4225 16.362 19.2678 16.0376 19.209C15.7132 19.1502 15.3786 19.1899 15.077 19.323C14.7754 19.4561 14.5215 19.6763 14.351 19.954C14.1805 20.2317 14.1016 20.5542 14.125 20.877V21C14.125 21.663 13.8616 22.2989 13.3928 22.7678C12.9239 23.2366 12.288 23.5 11.625 23.5C10.962 23.5 10.3261 23.2366 9.85725 22.7678C9.38839 22.2989 9.125 21.663 9.125 21V20.877C9.14842 20.5542 9.06954 20.2317 8.89901 19.954C8.72848 19.6763 8.47459 19.4561 8.173 19.323C7.87141 19.1899 7.53681 19.1502 7.21241 19.209C6.888 19.2678 6.58772 19.4225 6.353 19.653L6.293 19.713C6.10727 19.899 5.88675 20.0465 5.64385 20.1471C5.40095 20.2478 5.14003 20.2996 4.87645 20.2996C4.61286 20.2996 4.35194 20.2478 4.10904 20.1471C3.86614 20.0465 3.64562 19.899 3.45989 19.713C3.27415 19.5273 3.12667 19.3068 3.02603 19.0639C2.92539 18.821 2.87363 18.5601 2.87363 18.2965C2.87363 18.0329 2.92539 17.772 3.02603 17.5291C3.12667 17.2862 3.27415 17.0657 3.45989 16.88L3.519 16.821C3.74948 16.5863 3.90417 16.286 3.96299 15.9616C4.02181 15.6372 3.98211 15.3026 3.849 15.001C3.71589 14.6994 3.4957 14.4455 3.218 14.275C2.9403 14.1045 2.61782 14.0256 2.295 14.049V14C2.295 13.337 2.03161 12.7011 1.56274 12.2322C1.09388 11.7634 0.458 11.5 -0.205 11.5C-0.868 11.5 -1.50388 11.7634 -1.97274 12.2322C-2.44161 12.7011 -2.705 13.337 -2.705 14V14.123C-3.02882 14.0996 -3.3513 14.1785 -3.629 14.349C-3.9067 14.5195 -4.12689 14.7734 -4.26 15.075C-4.39311 15.3766 -4.43281 15.7112 -4.37399 16.0356C-4.31517 16.36 -4.16048 16.6603 -3.93 16.895L-3.871 16.954C-4.424 17.507 -4.424 18.393 -3.871 18.946L-3.93 19.005C-3.376 19.558 -3.376 20.444 -3.93 20.997L-3.871 21.056C-3.318 21.609 -3.318 22.495 -3.871 23.048L16.957 19.713L19.73 16.82C20.283 16.267 20.283 15.381 19.73 14.828L19.671 14.769C19.118 14.216 18.232 14.216 17.679 14.769L17.62 14.828C17.3853 15.0585 17.085 15.2132 16.7606 15.272C16.4362 15.3308 16.1016 15.2911 15.8 15.158C15.4984 15.0249 15.2445 14.8047 15.074 14.527C14.9035 14.2493 14.8246 13.9268 14.848 13.604V13.5C14.848 12.837 14.5846 12.2011 14.1157 11.7322C13.6469 11.2634 13.011 11 12.348 11C11.685 11 11.0491 11.2634 10.5803 11.7322C10.1114 12.2011 9.848 12.837 9.848 13.5V13.604C9.87142 13.9268 9.79254 14.2493 9.62201 14.527C9.45148 14.8047 9.19759 15.0249 8.896 15.158C8.59441 15.2911 8.25981 15.3308 7.93541 15.272C7.611 15.2132 7.31072 15.0585 7.076 14.828L7.017 14.769C6.464 14.216 5.578 14.216 5.025 14.769L4.966 14.828C4.73552 15.0627 4.43524 15.2174 4.11084 15.2762C3.78643 15.335 3.45183 15.2953 3.15024 15.1622C2.84865 15.0291 2.59476 14.8089 2.42423 14.5312C2.2537 14.2535 2.17482 13.931 2.19824 13.6082V13.5C2.19824 12.837 1.93485 12.2011 1.46599 11.7322C0.997124 11.2634 0.361245 11 -0.301755 11C-0.964755 11 -1.60063 11.2634 -2.0695 11.7322C-2.53836 12.2011 -2.80175 12.837 -2.80175 13.5V13.604C-3.12457 13.5806 -3.44705 13.6595 -3.72475 13.83C-4.00245 14.0005 -4.22264 14.2544 -4.35575 14.556C-4.48886 14.8576 -4.52856 15.1922 -4.46974 15.5166C-4.41092 15.841 -4.25623 16.1413 -4.02575 16.376L-3.96675 16.435C-3.41375 16.988 -3.41375 17.874 -3.96675 18.427L-4.02575 18.486C-4.57875 19.039 -4.57875 19.925 -3.96675 20.478L16.957 19.713L19.73 16.82C20.283 16.267 20.283 15.381 19.73 14.828L19.671 14.769C19.118 14.216 18.232 14.216 17.679 14.769L17.62 14.828C17.3853 15.0585 17.085 15.2132 16.7606 15.272C16.4362 15.3308 16.1016 15.2911 15.8 15.158C15.4984 15.0249 15.2445 14.8047 15.074 14.527C14.9035 14.2493 14.8246 13.9268 14.848 13.604V13.5C14.848 12.837 14.5846 12.2011 14.1157 11.7322C13.6469 11.2634 13.011 11 12.348 11C11.685 11 11.0491 11.2634 10.5803 11.7322C10.1114 12.2011 9.848 12.837 9.848 13.5V13.604C9.87142 13.9268 9.79254 14.2493 9.62201 14.527C9.45148 14.8047 9.19759 15.0249 8.896 15.158C8.59441 15.2911 8.25981 15.3308 7.93541 15.272C7.611 15.2132 7.31072 15.0585 7.076 14.828L7.017 14.769C6.464 14.216 5.578 14.216 5.025 14.769L4.966 14.828C4.73552 15.0627 4.43524 15.2174 4.11084 15.2762C3.78643 15.335 3.45183 15.2953 3.15024 15.1622C2.84865 15.0291 2.59476 14.8089 2.42423 14.5312C2.2537 14.2535 2.17482 13.931 2.19824 13.6082V13.5C2.19824 12.837 1.93485 12.2011 1.46599 11.7322C0.997124 11.2634 0.361245 11 -0.301755 11" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3>Персонализация</h3>
            <p>Алгоритмы адаптируются под ваши потребности, обеспечивая индивидуальный подход к вашей ситуации.</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                <path d="M21 16V8.00002C20.9996 7.6493 20.9071 7.30483 20.7315 7.00119C20.556 6.69754 20.3037 6.44539 20 6.27002L13 2.27002C12.696 2.09449 12.3511 2.00208 12 2.00208C11.6489 2.00208 11.304 2.09449 11 2.27002L4 6.27002C3.69626 6.44539 3.44398 6.69754 3.26846 7.00119C3.09294 7.30483 3.00036 7.6493 3 8.00002V16C3.00036 16.3508 3.09294 16.6952 3.26846 16.9989C3.44398 17.3025 3.69626 17.5547 4 17.73L11 21.73C11.304 21.9056 11.6489 21.998 12 21.998C12.3511 21.998 12.696 21.9056 13 21.73L20 17.73C20.3037 17.5547 20.556 17.3025 20.7315 16.9989C20.9071 16.6952 20.9996 16.3508 21 16Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M16.5 14.5C16.5 14.5 15.5 15.5 14 13.5C12.5 11.5 11.5 12.5 10.5 11.5C9.5 10.5 8 9.5 8 9.5" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3>Доступная стоимость</h3>
            <p>Качественная психологическая помощь по цене, доступной каждому. Первая консультация бесплатно.</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9.09 9.00002C9.3251 8.33167 9.78915 7.76813 10.4 7.40915C11.0108 7.05018 11.7289 6.91894 12.4272 7.03873C13.1255 7.15851 13.7588 7.52154 14.2151 8.06355C14.6713 8.60555 14.9211 9.29154 14.92 10C14.92 12 11.92 13 11.92 13" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 17H12.01" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3>Поддержка и обучение</h3>
            <p>Регулярные материалы и упражнения для самостоятельной работы над ментальным здоровьем.</p>
          </div>
        </div>
      </section>

      <!-- Секция "Как это работает" -->
      <section class="how-it-works-section">
        <h2>Как работает Serenity</h2>
        <p class="section-description">4 простых шага к улучшению вашего ментального состояния</p>
        <div class="steps-container">
          <div class="step">
            <div class="step-number">1</div>
            <h3>Регистрация</h3>
            <p>Создайте аккаунт, чтобы мы могли адаптировать помощь под ваши потребности</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>Опишите ситуацию</h3>
            <p>Расскажите о том, что вас беспокоит, в свободной форме</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>Получите поддержку</h3>
            <p>ИИ-психолог проанализирует вашу ситуацию и предложит помощь</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">4</div>
            <h3>Отслеживайте прогресс</h3>
            <p>Регулярно получайте отчеты о ваших успехах и рекомендации</p>
          </div>
        </div>
      </section>

      <!-- Новости и информация -->
      <section class="news-section">
        <h2>Последние новости и статьи</h2>
        <p class="section-description">Актуальные материалы о ментальном здоровье и психологии</p>
        <div class="news-grid">
          <div class="news-card">
            <div class="news-image">
              <img src="https://via.placeholder.com/300x200/4A5568/FFFFFF?text=Ментальное+Здоровье" alt="Новость 1"/>
            </div>
            <div class="news-content">
              <h3>10 способов снизить стресс</h3>
              <p>Практические советы по управлению стрессом в повседневной жизни. Узнайте, как небольшие изменения в распорядке дня могут значительно улучшить ваше состояние.</p>
              <div class="news-footer">
                <span class="news-date">12 ноября 2024</span>
                <a href="#" class="read-more">Читать →</a>
              </div>
            </div>
          </div>
          
          <div class="news-card">
            <div class="news-image">
              <img src="https://via.placeholder.com/300x200/4A5568/FFFFFF?text=Психология" alt="Новость 2"/>
            </div>
            <div class="news-content">
              <h3>Важность регулярной терапии</h3>
              <p>Почему регулярные сессии с психологом могут изменить вашу жизнь. Исследования показывают значительное улучшение качества жизни при систематической работе.</p>
              <div class="news-footer">
                <span class="news-date">8 ноября 2024</span>
                <a href="#" class="read-more">Читать →</a>
              </div>
            </div>
          </div>
          
          <div class="news-card">
            <div class="news-image">
              <img src="https://via.placeholder.com/300x200/4A5568/FFFFFF?text=ИИ+в+Медицине" alt="Новость 3"/>
            </div>
            <div class="news-content">
              <h3>ИИ в психиатрии: новые горизонты</h3>
              <p>Как искусственный интеллект помогает в диагностике и лечении ментальных расстройств. Обзор последних исследований и технологий.</p>
              <div class="news-footer">
                <span class="news-date">5 ноября 2024</span>
                <a href="#" class="read-more">Читать →</a>
              </div>
            </div>
          </div>
        </div>
        <div class="section-actions">
          <button class="outline-button">Все статьи</button>
        </div>
      </section>

      <!-- Секция с отзывами -->
      <section class="testimonials-section">
        <h2>Отзывы наших пользователей</h2>
        <p class="section-description">Реальные истории людей, которым помог Serenity</p>
        <div class="testimonials-container">
          <div class="testimonial-card">
            <div class="testimonial-content">
              <p>"Serenity помог мне справиться с паническими атаками, которые преследовали меня годами. Теперь я чувствую контроль над своей жизнью."</p>
            </div>
            <div class="testimonial-author">
              <div class="author-avatar">А</div>
              <div class="author-info">
                <h4>Анна К.</h4>
                <p>Пользуется 3 месяца</p>
              </div>
            </div>
          </div>
          
          <div class="testimonial-card">
            <div class="testimonial-content">
              <p>"Как студент медвуза, я скептически относился к ИИ в психологии, но Serenity доказал свою эффективность. Удобно и действительно работает."</p>
            </div>
            <div class="testimonial-author">
              <div class="author-avatar">М</div>
              <div class="author-info">
                <h4>Максим П.</h4>
                <p>Пользуется 5 месяцев</p>
              </div>
            </div>
          </div>
          
          <div class="testimonial-card">
            <div class="testimonial-content">
              <p>"После родов я столкнулась с тяжелой депрессией. Благодаря регулярным сессиям с ИИ-психологом, я постепенно возвращаюсь к нормальной жизни."</p>
            </div>
            <div class="testimonial-author">
              <div class="author-avatar">Е</div>
              <div class="author-info">
                <h4>Елена С.</h4>
                <p>Пользуется 2 месяца</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Секция призыва к действию -->
      <section class="cta-section">
        <div class="cta-container">
          <h2>Начните свой путь к mental wellbeing сегодня</h2>
          <p>Присоединяйтесь к тысячам пользователей, которые уже улучшили свое mental здоровье с помощью Serenity</p>
          <button class="cta-button primary" @click="scrollToChat">Начать бесплатно</button>
          <p class="cta-note">Первая консультация бесплатна. Никаких кредитных карт не требуется.</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  props: {
    page: {
      type: String,
      default: 'Serenity - Ваш психолог',
    },
  },
  data() {
    return {
      message: '',
    };
  },
  computed: {
    pageTitle() {
      return this.page;
    },
  },
  mounted() {
  },
  beforeUnmount() {
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
  },
  methods: {
    startChat() {
      if (this.message.trim()) {
        this.$router.push({
          path: '/chat',
          query: { message: this.message.trim() }
        });
      }
    },
    
    setExample(example) {
      this.message = example;
    },
    
    scrollToChat() {
      const element = document.getElementById('chat-section');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    },
    
    scrollToFeatures() {
      const element = document.getElementById('features-section');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  },
};
</script>

<style scoped>

.home-page {
  color: #e2e8f0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
}

.content {
  position: relative;
  z-index: 2;
  width: 100%;
  box-sizing: border-box;
  margin: 0;
  padding: 0rem 5vw;
}

section {
  margin-bottom: 8rem;
}

h2 {
  text-align: center;
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  margin-bottom: 1rem;
  color: #e2e8f0;
  font-weight: 700;
}

.section-description {
  text-align: center;
  color: #94a3b8;
  font-size: clamp(1rem, 2.5vw, 1.2rem);
  margin-bottom: 3rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* Герой-секция */
.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 85vh;
  padding: 4rem 0;
  gap: 3rem;
}

.hero-content {
  text-align: center;
  max-width: 900px;
}

.hero-content h1 {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: clamp(1.2rem, 2.5vw, 1.5rem);
  color: #cbd5e1;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-button {
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.cta-button.primary {
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  color: white;
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(128, 90, 213, 0.4);
}

.cta-button.secondary {
  background: transparent;
  color: #e2e8f0;
  border: 1px solid #805AD5;
}

.cta-button.secondary:hover {
  background: rgba(128, 90, 213, 0.1);
  transform: translateY(-2px);
}

.hero-visual {
  position: relative;
  width: 100%;
  max-width: 1000px;
  height: 350px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.floating-card {
  position: absolute;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 200px;
  transition: all 0.5s ease;
}

.floating-card:hover {
  transform: translateY(-5px);
}

.card-1 {
  top: 10%;
  left: 5%;
  animation: float 6s ease-in-out infinite;
}

.card-2 {
  top: 60%;
  right: 5%;
  transform: translateY(-50%);
  animation: float 7s ease-in-out infinite 1s;
}

.card-3 {
  bottom: 5%;
  left: 45%;
  transform: translateX(-50%);
  animation: float 8s ease-in-out infinite 2s;
}

.card-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Секция с чат-интерфейсом */
.chat-section {
  padding: 4rem 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, rgba(128, 90, 213, 0.05) 0%, rgba(102, 126, 234, 0.05) 100%);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.chat-container {
  width: 100%;
  max-width: 700px;
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
  text-align: center;
}

.chat-container h2 {
  font-size: clamp(1.5rem, 3vw, 2rem);
  margin-bottom: 0.5rem;
}

.chat-container .section-description {
  margin-bottom: 2rem;
}

.input-container {
  width: 100%;
}

.input-wrapper {
  display: flex;
  background: #1e293b;
  border-radius: 12px;
  padding: 0.5rem;
  border: 1px solid #475569;
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: #805AD5;
  box-shadow: 0 0 0 2px rgba(128, 90, 213, 0.5);
}

.chat-input {
  flex-grow: 1;
  background: transparent;
  border: none;
  color: white;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  outline: none;
}

.chat-input::placeholder {
  color: #64748b;
}

.send-button {
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  border: none;
  border-radius: 8px;
  color: white;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 20px rgba(128, 90, 213, 0.4);
}

.send-button svg {
  color: white;
}

.examples {
  margin-top: 1.5rem;
  text-align: left;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
}

.example-text {
  color: #94a3b8;
  font-size: 0.9rem;
}

.example-item {
  background: rgba(128, 90, 213, 0.1);
  color: #805AD5;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.example-item:hover {
  background: rgba(128, 90, 213, 0.2);
}

/* Секция с преимуществами */
.features-section {
  padding: 4rem 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 2.5rem;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.feature-card:hover {
  transform: translateY(-10px);
  border-color: #805AD5;
}

.feature-icon {
  margin: 0 auto 1.5rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(128, 90, 213, 0.1);
  border-radius: 50%;
}

.feature-icon svg {
  width: 40px;
  height: 40px;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #e2e8f0;
}

.feature-card p {
  color: #94a3b8;
}

/* Секция "Как это работает" */
.how-it-works-section {
  padding: 4rem 0;
}

.steps-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  max-width: 1100px;
  margin: 0 auto;
  position: relative;
}

.step {
  flex: 1;
  min-width: 200px;
  text-align: center;
  padding: 0 1rem;
  position: relative;
  margin-bottom: 2rem;
}

.step-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 1.5rem;
}

.step h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  color: #e2e8f0;
}

.step p {
  color: #94a3b8;
  line-height: 1.6;
}

.step-arrow {
  color: #805AD5;
  font-size: 2rem;
  margin: 2rem 0.5rem 0;
  display: none;
}

/* Новости и информация */
.news-section {
  padding: 4rem 0;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.news-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.news-card:hover {
  transform: translateY(-10px);
  border-color: #805AD5;
}

.news-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.news-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.news-content h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #e2e8f0;
}

.news-content p {
  color: #94a3b8;
  flex-grow: 1;
  margin-bottom: 1.5rem;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.news-date {
  font-size: 0.9rem;
  color: #64748b;
}

.read-more {
  color: #805AD5;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.read-more:hover {
  color: #667eea;
}

.section-actions {
  display: flex;
  justify-content: center;
  margin-top: 3rem;
}

.outline-button {
  background: transparent;
  border: 1px solid #805AD5;
  color: #cbd5e1;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.outline-button:hover {
  background: rgba(128, 90, 213, 0.1);
  transform: translateY(-2px);
}

/* Секция с отзывами */
.testimonials-section {
  padding: 4rem 0;
}

.testimonials-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.testimonial-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 2.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.testimonial-card:hover {
  transform: translateY(-10px);
  border-color: #805AD5;
}

.testimonial-content {
  margin-bottom: 1.5rem;
}

.testimonial-content p {
  color: #e2e8f0;
  font-style: italic;
  line-height: 1.6;
}

.testimonial-author {
  display: flex;
  align-items: center;
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
  margin-right: 1rem;
  flex-shrink: 0;
}

.author-info h4 {
  margin: 0;
  color: #e2e8f0;
}

.author-info p {
  margin: 0;
  color: #94a3b8;
  font-size: 0.9rem;
}

/* Секция призыва к действию */
.cta-section {
  background: linear-gradient(135deg, rgba(128, 90, 213, 0.1) 0%, rgba(102, 126, 234, 0.1) 100%);
  border-radius: 20px;
  padding: 4rem 2rem;
  text-align: center;
  margin: 6rem auto;
  max-width: 900px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.cta-container h2 {
  margin-bottom: 1.5rem;
}

.cta-container > p {
  color: #cbd5e1;
  font-size: 1.2rem;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.cta-note {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-top: 1.5rem;
}

/* Адаптивность */
@media (min-width: 768px) {
  .hero-section {
    flex-direction: row;
    text-align: left;
    align-items: center;
    justify-content: space-between;
  }
  
  .hero-content {
    text-align: left;
    flex: 1;
  }
  
  .hero-actions {
    justify-content: flex-start;
  }
  
  .hero-visual {
    flex: 1;
    height: 400px;
  }
  
  .step-arrow {
    display: block;
  }
  
  .steps-container {
    justify-content: center;
    gap: 1.5rem;
  }
  
  .step {
    flex-basis: 20%;
    min-width: auto;
    max-width: 250px;
    margin-bottom: 0;
  }
}

@media (max-width: 768px) {
  .steps-container {
    flex-direction: column;
    align-items: center;
  }
  
  .step {
    margin-bottom: 3rem;
  }
  
  .floating-card {
    position: relative;
    margin-bottom: 1.5rem;
    left: auto;
    right: auto;
    top: auto;
    bottom: auto;
    transform: none;
  }
  
  .hero-visual {
    flex-direction: column;
    height: auto;
  }
  
  .testimonials-container {
    grid-template-columns: 1fr;
  }
  
  .cta-container {
    padding: 3rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .hero-actions {
    flex-direction: column;
  }
  
  .cta-button {
    width: 100%;
  }
  
  .news-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>