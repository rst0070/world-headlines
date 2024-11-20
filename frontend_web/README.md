# Frontend-web

## Project Structure
It will be like below.  
```
src/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── countries/
│   │       │   └── route.ts
│   │       └── headlines/
│   │           └── route.ts
│   └── page.tsx
├── components/
│   ├── country/
│   │   ├── CountryDescElement.tsx
│   │   ├── CountryDescContainer.tsx
│   │   └── index.ts
│   └── layout/
│       ├── MainHeader.tsx
│       ├── MainDescription.tsx
│       └── index.ts
├── types/
│   ├── country.ts
│   └── headline.ts
├── services/
│   ├── api/
│   │   ├── countryService.ts
│   │   └── headlineService.ts
│   └── index.ts
└── utils/
    ├── constants.ts
    └── helpers.ts
```
- `src/app/api` defines backend api of next.js
- `src/services/api` defines service layer from client side which helps to use next.js backend api
  

## Notes
- deployment
    - https://kladds.medium.com/next-js-vercel-for-rapid-and-free-application-deployment-7a45da08ff07
