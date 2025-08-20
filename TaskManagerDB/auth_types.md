### 1. Basic

HTTP / HTTPS
```json
{
  "headers": {
    "Authorization": "Basic ewfkjb32r2je"
  }
}
```

### 2. Digest 
Сервер => nonce
Браузер => MD5 (вычисляется через nonce)

MitM --> man-in-the-middle

### (3. NTLM)

### (4. Negotiate)

## Forms auth-n
есть какая-то форма:
```html
<form method="POST" url="/auth">
  <input type="text" name="username">
  <input type="password" name="password">
  <button> Войти </button>
</form>
```
Сервер создает session token => browser cookies
Клиент при след.запросах отправляет автоматически session token

```json
{
  "headers": {
    "Cookie": "token=ewfkjb32r2je"
  }
}
```
Два способа создания токена:
1. Идентификатор сессии, который хранится в памяти сервера либо в базе данных (либо ОЗУ типа redis)
2. Зашифрованный и/или подписанный объект + период действия.

## Как передавать user-pass?
1. URL query => небезопасно, тк их можно перехватывать и они запоминаются браузерами
2. Request BODY => безопасный вариант, но применим только к запросам с телом (POST, PUT, PATCH)
3. HTTP header – оптимально, можно использовать стандартный заголовок или другие произвольные заголовки