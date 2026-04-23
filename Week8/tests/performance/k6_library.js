import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export const options = {
  scenarios: {
    read_heavy: {
      executor: 'constant-vus',
      exec: 'readHeavy',
      vus: 10,
      duration: '30s',
    },
    borrow_return_flow: {
      executor: 'constant-vus',
      exec: 'borrowReturnFlow',
      vus: 5,
      duration: '30s',
      startTime: '5s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<500'],
  },
};

export function setup() {
  for (let i = 0; i < 3; i += 1) {
    http.post(
      `${BASE_URL}/books`,
      JSON.stringify({
        title: `Load Test Book ${i}`,
        author: 'k6',
        total_quantity: 50,
      }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  }
}

export function readHeavy() {
  const res = http.get(`${BASE_URL}/books`);
  check(res, {
    'GET /books status is 200': (r) => r.status === 200,
  });
  sleep(0.2);
}

export function borrowReturnFlow() {
  const booksRes = http.get(`${BASE_URL}/books`);
  const books = booksRes.status === 200 ? booksRes.json() : [];
  if (!books.length) {
    sleep(0.2);
    return;
  }

  const target = books[Math.floor(Math.random() * books.length)];
  const borrower = `user_${__VU}_${__ITER}`;

  const borrowRes = http.post(
    `${BASE_URL}/borrows`,
    JSON.stringify({ book_id: target.id, borrower_name: borrower }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(borrowRes, {
    'POST /borrows status valid': (r) => r.status === 200 || r.status === 400,
  });

  if (borrowRes.status === 200) {
    const borrow = borrowRes.json();
    const returnRes = http.post(`${BASE_URL}/borrows/${borrow.id}/return`);
    check(returnRes, {
      'POST /borrows/{id}/return status is 200': (r) => r.status === 200,
    });
  }

  sleep(0.2);
}
