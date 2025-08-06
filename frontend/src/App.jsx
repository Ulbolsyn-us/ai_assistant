import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home';
import MessageList from './pages/MessageList';
import Templates from './pages/Templates';
import Settings from './pages/Settings';
import HrInbox from './pages/HrInbox';
import Invites from './pages/Invites'

function App() {
    return (
        <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/message_list" element={<MessageList />} />
                    <Route path="/templates" element={<Templates />} />
                    <Route path="/hr_inbox" element={<HrInbox />} />
                    <Route path="/invites" element={<Invites />} />
                    <Route path="/settings" element={<Settings />} />
                </Routes>
        </BrowserRouter>
    );
}

export default App;

