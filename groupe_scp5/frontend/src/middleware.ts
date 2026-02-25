import createMiddleware from "next-intl/middleware";
import { routing }       from "./i18n/routing";

export default createMiddleware(routing);

export const config = {
  matcher: [
    // Match the root
    "/",
    // Match all pathnames except _next, api, static files
    "/(fr|en|crm)/:path*",
    "/((?!_next|_vercel|.*\\..*).*)",
  ],
};
