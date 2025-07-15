


from typing import List

from ufo.module.basic import BaseSession


class PCRemoteClientManager:
    """The manager for the PC-AGENT-REMOTE clients."""
    def __init__(self, sessions):
        """Initialize a batch PC-AGENT-REMOTE client."""
        self.sessions = sessions
    def run_all(self):
        """Run the batch PC-AGENT-REMOTE client."""
        for session in self.session_list:
            session.run()

    @property
    def session_list(self) -> List[BaseSession]:
        """
        Get the session list.
        :return: The session list.
        """
        return self._session_list

    def add_session(self, session: BaseSession) -> None:
        """
        Add a session to the session list.
        :param session: The session to add.
        """
        self._session_list.append(session)

    def next_session(self) -> BaseSession:
        """
        Get the next session.
        :return: The next session.
        """
        return self._session_list.pop(0)
