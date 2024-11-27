import type { MetadataRoute } from 'next'
import { environment } from '@/environment'
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: '/private/',
    },
    sitemap: `${environment.siteUrlPrefix}/sitemap.xml`,
  }
}