/**
 * Validates a website URL against the rules in 08_api_contracts.md
 * ("Website URL — Must be HTTPS when possible, Must be publicly
 * accessible"). Public reachability can only be confirmed by the backend,
 * so this checks what the client reasonably can: that the string parses
 * as an absolute http(s) URL with a real host.
 *
 * Returns an error message to display, or `null` if the URL is valid.
 */
export function validateWebsiteUrl(rawValue: string): string | null {
  const value = rawValue.trim();

  if (!value) {
    return "Enter a website URL.";
  }

  let url: URL;
  try {
    url = new URL(value);
  } catch {
    return "Enter a full URL, including https://";
  }

  if (url.protocol !== "http:" && url.protocol !== "https:") {
    return "URL must start with http:// or https://";
  }

  if (!url.hostname || !url.hostname.includes(".")) {
    return "Enter a valid domain, e.g. https://company.com";
  }

  return null;
}
