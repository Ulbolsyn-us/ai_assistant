import { useEffect, useState } from "react";
import axios from "axios";

function HrInbox() {
    const [messages, setHrInbox] = useState([])
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchHrInbox();
    }, [])

    const fetchHrInbox = async () => {
        try {
            const res = await axios.get("http://localhost:8000/hr-inbox");
            setHrInbox(res.data);
            setLoading(false);
        } catch (err) {
            console.error("Ошибка при получении шаблонов:", err)
        }
    };

    if (loading) return  <p>Загрузка обращений...</p>

    return (
        <div className="m-12">
            <h2 className="hd p-0">Обращения, требующие внимания HR</h2>
                {messages.length > 0 ? (
                    messages.map((message, index) => (
                        <div className="my-4 max-w-l p-6 rounded-lg dark:bg-gray-500" key={index}>
                            <strong>⏱ {message.timestamp}</strong>
                            <div><b>Пользователь:</b> {message.user_message}</div>
                            <div><b>Бот:</b> {message.bot_reply}</div>
                        </div>
                    ))
                ) : (
                    <p>Нет новых обращений.</p>
                )}
            <button className="py-2.5 px-5 me-2 mb-2 flex items-center text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-4">
  <path strokeLinecap="round" strokeLinejoin="round" d="m18.75 4.5-7.5 7.5 7.5 7.5m-6-15L5.25 12l7.5 7.5" />
</svg>

                <a href="/" className="pl-2">Назад в главный меню</a>
            </button>
        </div>
    )
}

export default HrInbox