
CREATE TABLE IF NOT EXISTS customers (
    id BIGSERIAL PRIMARY KEY,
    telegram_user_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(100),
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    phone VARCHAR(30),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS conversations (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(id),
    chat_id BIGINT UNIQUE NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'bot',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    conversation_id BIGINT NOT NULL REFERENCES conversations(id),
    telegram_message_id BIGINT,
    direction VARCHAR(10) NOT NULL,
    message_type VARCHAR(30) NOT NULL DEFAULT 'text',
    content TEXT,
    file_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT messages_direction_check
        CHECK (direction IN ('incoming', 'outgoing'))
);

CREATE TABLE IF NOT EXISTS quotes (
    id BIGSERIAL PRIMARY KEY,
    conversation_id BIGINT NOT NULL REFERENCES conversations(id),
    calculator_type VARCHAR(100) NOT NULL,
    input_amount NUMERIC(20, 8) NOT NULL,
    result_data JSONB NOT NULL,
    rate_snapshot JSONB NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'quoted',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conversations_customer
    ON conversations(customer_id);

CREATE INDEX IF NOT EXISTS idx_messages_conversation
    ON messages(conversation_id);

CREATE INDEX IF NOT EXISTS idx_quotes_conversation
    ON quotes(conversation_id);

CREATE INDEX IF NOT EXISTS idx_customers_username
    ON customers(username);

-- ============================================================
-- OPERAÇÕES DE REMESSA
-- ============================================================

CREATE TABLE IF NOT EXISTS operations (
    id BIGSERIAL PRIMARY KEY,
    conversation_id BIGINT NOT NULL
        REFERENCES conversations(id),

    status VARCHAR(30) NOT NULL DEFAULT 'created',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- COTAÇÕES VINCULADAS ÀS OPERAÇÕES
-- ============================================================

CREATE TABLE IF NOT EXISTS operation_quotes (
    id BIGSERIAL PRIMARY KEY,

    operation_id BIGINT NOT NULL
        REFERENCES operations(id),

    quote_id BIGINT NOT NULL
        REFERENCES quotes(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT operation_quotes_unique
        UNIQUE (operation_id, quote_id)
);


-- ============================================================
-- ÍNDICES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_operations_conversation
    ON operations(conversation_id);

CREATE INDEX IF NOT EXISTS idx_operations_status
    ON operations(status);

CREATE INDEX IF NOT EXISTS idx_operation_quotes_operation
    ON operation_quotes(operation_id);

CREATE INDEX IF NOT EXISTS idx_operation_quotes_quote
    ON operation_quotes(quote_id);
