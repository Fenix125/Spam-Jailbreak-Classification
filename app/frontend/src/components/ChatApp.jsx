import { useEffect, useMemo, useRef, useState, useCallback } from "react";
import { sendAgentPrompt } from "../api";
import "./ChatApp.css";

function uuid() {
    return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export default function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [pending, setPending] = useState(false);
    const [error, setError] = useState(null);

    const scrollerRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => {
        const el = scrollerRef.current;
        if (!el) return;
        el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
    }, [messages.length, pending]);

    useEffect(() => {
        const el = inputRef.current;
        if (!el) return;
        el.style.height = "0px";
        const next = Math.min(240, el.scrollHeight);
        el.style.height = next + "px";
    }, [input]);

    const canSend = useMemo(
        () => input.trim().length > 0 && !pending,
        [input, pending]
    );

    const handleSend = useCallback(async () => {
        const text = input.trim();
        if (!text) return;

        const userMsg = {
            id: uuid(),
            role: "user",
            content: text,
            ts: Date.now(),
        };
        setMessages((m) => [...m, userMsg]);
        setInput("");
        setPending(true);
        setError(null);

        try {
            const reply = await sendAgentPrompt(text);
            const botMsg = {
                id: uuid(),
                role: "assistant",
                content: String(reply ?? ""),
                ts: Date.now(),
            };
            setMessages((m) => [...m, botMsg]);
        } catch (e) {
            setError(e?.message || "Request failed");
        } finally {
            setPending(false);
        }
    }, [input]);

    function onKeyDown(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (canSend) handleSend();
        }
    }

    return (
        <div className="chat">
            <header className="chat__header">
                <div className="chat__headerWrap">
                    <div className="chat__title">My Agent</div>
                    <div className="chat__subtitle">Chat with your agent</div>
                </div>
            </header>

            <main ref={scrollerRef} className="chat__messages">
                {messages.length === 0 && (
                    <div className="chat__empty">
                        Say hi 👋 or ask me to classify spam/ham or to provide
                        information about Mykhailo Ivasiuk.
                    </div>
                )}

                {messages.map((m) => (
                    <Message key={m.id} role={m.role} content={m.content} />
                ))}

                {pending && <TypingBubble />}
                {error && (
                    <div className="chat__error" role="alert">
                        {error}
                    </div>
                )}
            </main>

            <footer className="chat__composer">
                <div className="composer">
                    <textarea
                        ref={inputRef}
                        className="composer__input"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={onKeyDown}
                        placeholder="Type a message…"
                        rows={1}
                        maxLength={8000}
                        aria-label="Message"
                    />
                    <button
                        className="composer__send"
                        onClick={handleSend}
                        disabled={!canSend}
                        aria-label="Send message"
                    >
                        <svg
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                            aria-hidden="true"
                        >
                            <path d="M3.4 20.6L22 12 3.4 3.4 3 10l10 2-10 2z" />
                        </svg>
                    </button>
                </div>
                <div className="composer__hint">
                    Enter to send · Shift+Enter for newline
                </div>
            </footer>
        </div>
    );
}

function Message({ role, content }) {
    const isUser = role === "user";
    return (
        <div className={`msg ${isUser ? "msg--user" : "msg--assistant"}`}>
            <div
                className={`msg__avatar ${
                    isUser ? "msg__avatar--user" : "msg__avatar--assistant"
                }`}
            >
                {isUser ? "🙂" : "🤖"}
            </div>
            <div className="msg__bubble">
                <div className="msg__meta">{isUser ? "You" : "Assistant"}</div>
                <div className="msg__text">{content}</div>
            </div>
        </div>
    );
}

function TypingBubble() {
    return (
        <div className="msg msg--assistant">
            <div className="msg__avatar msg__avatar--assistant">🤖</div>
            <div className="msg__bubble">
                <div className="typing">
                    <span className="typing__dot" />
                    <span className="typing__dot" />
                    <span className="typing__dot" />
                </div>
            </div>
        </div>
    );
}
