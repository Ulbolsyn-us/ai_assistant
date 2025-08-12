import { useEffect, useState } from "react";
import axios from "axios";

function MessageList() {
    const [ messages, setMessages ] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchMessages();
    }, []);

    const fetchMessages = async () => {
        try {
            const res = await axios.get(`${import.meta.env.VITE_API_URL}/messages`);
            setMessages(res.data);
            setLoading(false);
        } catch (err) {
            console.error("Ошибка при получении сообщений:", err);
        }
    };

    if (loading) return <p>Загрузка шаблонов...</p>

    return (
        <div className="m-12">
            <h2 className="hd p-0"> История сообщений</h2>
            {messages.length === 0 ? (
                <p>Сообщений пока нет.</p>
            ) : (
                <div className="relative overflow-x-auto my-4">
                    <table className="w-full text-base text-left text-gray-500 dark:text-gray-400 rtl:text-right" style={{ width: "100%", borderCollapse: "collapse"}}>
                        <thead className="text-base text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                            <tr>
                                <th scope="col" className="px-6 py-3">Пользователь</th>
                                <th scope="col" className="px-6 py-3">Сообщение</th>
                                <th scope="col" className="px-6 py-3">Ответ бота</th>
                                <th scope="col" className="px-6 py-3">Нужен оператор?</th>
                                <th scope="col" className="px-6 py-3">Forward to HR?</th>
                            </tr>
                        </thead>
                        <tbody>
                            {messages.map((msg) => (
                                <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200" key={msg.id}>
                                    <td className="px-6 py-4">{msg.user_id}</td>
                                    <td className="px-6 py-4">{msg.user_message}</td>
                                    <td className="px-6 py-4">{msg.bot_reply}</td>
                                    <td className="px-6 py-4">{msg.needs_operator ? "✅" : "—"}</td>
                                    <td className="px-6 py-4">{msg.forwarded_to_hr ? "✅" : "—"}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
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

export default MessageList;
