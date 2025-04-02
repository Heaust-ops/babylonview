class Comms {
  private socket: WebSocket;
  private messageListeners: Array<(msg: string) => void> = [];
  private messageQueue: string[] = [];
  private isOpen: boolean = false;

  constructor(url: string) {
    this.socket = new WebSocket(url);

    this.socket.addEventListener("open", () => {
      console.log("WebSocket connected.");
      this.isOpen = true;

      while (this.messageQueue.length > 0) {
        const msg = this.messageQueue.shift();
        if (msg !== undefined) {
          this.socket.send(msg);
        }
      }
    });

    this.socket.addEventListener("message", (event: MessageEvent) => {
      this.messageListeners.forEach((listener) => listener(event.data));
    });

    this.socket.addEventListener("close", () => {
      console.log("WebSocket closed.");
      this.isOpen = false;
    });

    this.socket.addEventListener("error", (error) => {
      console.error("WebSocket error:", error);
    });
  }

  /**
   * Sends a message through the WebSocket.
   * If the connection is not yet open, the message is queued.
   * @param message The message to send.
   */
  public send(message: string): void {
    if (this.isOpen) {
      this.socket.send(message);
    } else {
      console.warn("WebSocket is not open. Queueing message.");
      this.messageQueue.push(message);
    }
  }

  /**
   * Adds a listener for incoming messages.
   * @param listener Callback to process messages.
   */
  public addMessageListener(listener: (msg: string) => void): void {
    this.messageListeners.push(listener);
  }
}

export { Comms };
