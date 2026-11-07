/**
 * Safely format API errors returned by FastAPI / Pydantic / network responses.
 * Prevents [object Object] from ever leaking to the UI.
 */
export const formatApiError = (err: any, fallback: string = 'Operation failed'): string => {
  if (!err) return fallback;
  if (typeof err === 'string') return err;

  // Handle FastAPI HTTPException detail as string
  if (typeof err.detail === 'string') return err.detail;

  // Handle FastAPI / Pydantic v2 422 validation error array:
  // [{ loc: ['body', 'slug'], msg: "String should match pattern '^[a-zA-Z0-9_\\-]+$'", type: '...' }]
  if (Array.isArray(err.detail)) {
    const formatted = err.detail
      .map((item: any) => {
        if (typeof item === 'string') return item;
        const field = Array.isArray(item.loc)
          ? item.loc.filter((l: any) => l !== 'body').join('.')
          : '';
        const msg = item.msg || item.message || JSON.stringify(item);
        return field ? `${field}: ${msg}` : msg;
      })
      .filter(Boolean)
      .join(' | ');

    if (formatted) return formatted;
  }

  // Handle object detail e.g. { message: "..." }
  if (err.detail && typeof err.detail === 'object') {
    if (typeof err.detail.message === 'string') return err.detail.message;
    if (typeof err.detail.error === 'string') return err.detail.error;
    try {
      return JSON.stringify(err.detail);
    } catch {
      return fallback;
    }
  }

  // Handle standard JavaScript Error message
  if (typeof err.message === 'string' && err.message !== '[object Object]') {
    return err.message;
  }

  return fallback;
};

