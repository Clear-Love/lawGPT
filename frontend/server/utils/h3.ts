import { H3Event } from "h3";

export function setResStatus(event: H3Event, code: number, message: string) {
  event.node.res.statusCode = code;
  event.node.res.statusMessage = message;
}

export async function errorHandler(event: H3Event, e: any) {
  if (e.response?.data) {
    setResStatus(event, e.response.status, e.response.data.statusText);

    let isStreamNull = true;

    for await (const data of e.response.data) {
      isStreamNull = false;
      const message = data.toString();
      try {
        const parsed = JSON.parse(message);
        return parsed;
      } catch (error) {
        return message;
      }
    }

    if (isStreamNull) {
      return e;
    }
  } else {
    return e;
  }
}
